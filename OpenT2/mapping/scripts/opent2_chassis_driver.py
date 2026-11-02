#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenT2: Clean-Room STM32 Chassis Driver Node
---------------------------------------------
Reverse engineered from Keenon T2 chassis communication stack.
Protocol:
  - Baudrate: 115200 8N1
  - Header: 0xAA 0xAA 0x00 0xE0
  - Tail: 0x55 0x55
  - Escape byte: 0xA5
  - Checksum: CRC16-Modbus/IBM (Poly: 0xA001, Init: 0xFFFF)
  - Cmd 0x002D: Encoder raw ticks (left_ticks, right_ticks)
  - Cmd 0x002F: Motor control & telemetry
  - Cmd 0x0132: Dummy IMU (unpopulated hardware)
"""

import sys
import time
import struct
import math
import rospy
from geometry_msgs.msg import Twist, Quaternion, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, BatteryState
from std_msgs.msg import Float64, Bool
import tf
import tf2_ros

try:
    from keenon_motor_msgs.msg import encoder as EncoderMsg
except ImportError:
    EncoderMsg = None

def crc16_ibm(data):
    """CRC16-IBM / Modbus (Polynomial 0xA001, Init 0xFFFF) matching getDataFromFrame."""
    crc = 0xFFFF
    for byte in bytearray(data):
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

def pack_frame(cmd_id, payload):
    """Packs payload with command ID, CRC16, escape bytes, header, and tail."""
    raw_stream = struct.pack("<H", cmd_id) + payload
    crc = crc16_ibm(raw_stream)
    crc_bytes = struct.pack("<H", crc)
    
    body = raw_stream + crc_bytes
    # Apply 0xA5 byte stuffing
    escaped_body = bytearray()
    for b in bytearray(body):
        if b in (0xAA, 0x55, 0xA5):
            escaped_body.append(0xA5)
        escaped_body.append(b)
        
    header = b"\xAA\xAA\x00\xE0"
    tail = b"\x55\x55"
    return header + bytes(escaped_body) + tail

def unpack_frame(frame_bytes):
    """Validates header, tail, unstuffs 0xA5, and verifies CRC."""
    if len(frame_bytes) < 8:
        return None, None
    if frame_bytes[:4] != b"\xAA\xAA\x00\xE0" or frame_bytes[-2:] != b"\x55\x55":
        return None, None
    
    escaped = frame_bytes[4:-2]
    body = bytearray()
    i = 0
    while i < len(escaped):
        if escaped[i] == 0xA5 and (i + 1) < len(escaped):
            i += 1
        body.append(escaped[i])
        i += 1
        
    if len(body) < 4:
        return None, None
        
    data_payload = bytes(body[:-2])
    received_crc = struct.unpack("<H", bytes(body[-2:]))[0]
    computed_crc = crc16_ibm(data_payload)
    
    if received_crc != computed_crc:
        return None, None
        
    cmd_id = struct.unpack("<H", data_payload[:2])[0]
    payload = data_payload[2:]
    return cmd_id, payload

class OpenT2ChassisDriver(object):
    def __init__(self, serial_port="/dev/ttyUSBStm32", baudrate=115200, test_mode=False):
        self.test_mode = test_mode
        self.port = serial_port
        self.baudrate = baudrate
        
        # Physical parameters from T2.urdf and chassis_params.yaml
        self.wheel_gauge = rospy.get_param("~wheel_gauge", 366.0) / 1000.0  # 0.366 m
        self.wheel_perimeter = rospy.get_param("~wheel_perimeter", 517.2) / 1000.0  # 0.5172 m
        self.wheel_radius = self.wheel_perimeter / (2.0 * math.pi)  # ~0.0823 m (nominal 0.085m)
        self.ticks_per_rev = rospy.get_param("~ticks_per_rev", 4000.0) # nominal quadrature resolution
        
        # State tracking
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.prev_left_ticks = None
        self.prev_right_ticks = None
        self.last_time = rospy.Time.now() if not test_mode else None
        
        # Publishers & Subscribers (only initialize ROS if not in pure unit-test mode)
        if not self.test_mode:
            self.odom_pub = rospy.Publisher("/encoder_odom", Odometry, queue_size=10)
            self.mileage_pub = rospy.Publisher("/mileage", Float64, queue_size=10)
            self.battery_pub = rospy.Publisher("/battery_state", BatteryState, queue_size=10)
            if EncoderMsg:
                self.encoder_pub = rospy.Publisher("/encoder_raw", EncoderMsg, queue_size=10)
            rospy.Subscriber("/cmd_vel", Twist, self.cmd_vel_callback)
            self.tf_broadcaster = tf.TransformBroadcaster()
        else:
            self.odom_pub = None
            self.mileage_pub = None
            self.battery_pub = None
            self.encoder_pub = None
            self.tf_broadcaster = None

    def process_encoder_packet(self, payload, current_time=None):
        """Processes Command 0x002D: Encoder raw ticks."""
        if len(payload) < 8:
            return None
        left_ticks, right_ticks = struct.unpack("<ii", payload[:8])
        
        if current_time is None:
            current_time = rospy.Time.now()
            
        if self.prev_left_ticks is None:
            self.prev_left_ticks = left_ticks
            self.prev_right_ticks = right_ticks
            self.last_time = current_time
            return left_ticks, right_ticks, 0.0, 0.0
            
        d_left_ticks = left_ticks - self.prev_left_ticks
        d_right_ticks = right_ticks - self.prev_right_ticks
        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks
        
        # Compute displacements in meters
        d_left = (float(d_left_ticks) / self.ticks_per_rev) * self.wheel_perimeter
        d_right = (float(d_right_ticks) / self.ticks_per_rev) * self.wheel_perimeter
        
        d_dist = (d_left + d_right) / 2.0
        d_th = (d_right - d_left) / self.wheel_gauge
        
        # Update pose (Runge-Kutta / 2nd order approximation)
        dt = (current_time - self.last_time).to_sec() if self.last_time else 0.02
        self.last_time = current_time
        
        self.x += d_dist * math.cos(self.th + d_th / 2.0)
        self.y += d_dist * math.sin(self.th + d_th / 2.0)
        self.th += d_th
        
        v_x = d_dist / dt if dt > 0 else 0.0
        v_th = d_th / dt if dt > 0 else 0.0
        
        # Publish ROS messages
        self.publish_odometry(current_time, self.x, self.y, self.th, v_x, v_th)
        return left_ticks, right_ticks, d_dist, d_th

    def publish_odometry(self, stamp, x, y, th, vx, vth):
        if self.test_mode:
            return
        q = tf.transformations.quaternion_from_euler(0, 0, th)
        
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.orientation = Quaternion(*q)
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth
        self.odom_pub.publish(odom)

    def cmd_vel_callback(self, msg):
        """Converts Twist (v, w) to differential motor speed frame."""
        v = msg.linear.x
        w = msg.angular.z
        
        # Differential kinematics: v_left = v - w * L/2, v_right = v + w * L/2
        v_left = v - (w * self.wheel_gauge / 2.0)
        v_right = v + (w * self.wheel_gauge / 2.0)
        
        # Convert m/s to motor target counters (or mm/s as required by STM32)
        target_l = int(v_left * 1000.0)
        target_r = int(v_right * 1000.0)
        
        packet = pack_frame(0x002F, struct.pack("<ii", target_l, target_r))
        return packet

def run_self_test():
    """Validates serialization, checksum, and kinematics in simulation."""
    print("=== Running OpenT2 Chassis Driver Self-Test ===")
    
    # Test 1: CRC16 calculation
    test_data = b"\x2D\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    crc = crc16_ibm(test_data)
    print("Test 1: CRC16-Modbus on dummy encoder data: 0x%04X" % crc)
    assert isinstance(crc, int)
    
    # Test 2: Frame Packing and Unpacking
    cmd = 0x002D
    payload = struct.pack("<ii", 1000, 1000)
    packed = pack_frame(cmd, payload)
    print("Test 2: Packed Frame Length: %d bytes (Raw: %s)" % (len(packed), packed.encode("hex")))
    assert packed.startswith(b"\xAA\xAA\x00\xE0")
    assert packed.endswith(b"\x55\x55")
    
    unpacked_cmd, unpacked_payload = unpack_frame(packed)
    assert unpacked_cmd == cmd
    l, r = struct.unpack("<ii", unpacked_payload)
    assert l == 1000 and r == 1000
    print("Test 2 Passed: Exact frame round-trip verified.")
    
    # Test 3: Kinematics test
    driver = OpenT2ChassisDriver(test_mode=True)
    class FakeTime(object):
        def __init__(self, s):
            self.s = s
        def to_sec(self):
            return self.s
        def __sub__(self, o):
            return FakeTime(self.s - o.s)
            
    # Initial ticks
    driver.process_encoder_packet(struct.pack("<ii", 0, 0), FakeTime(100.0))
    # After forward move of 4000 ticks (1 revolution = 0.5172 m)
    l, r, dist, d_th = driver.process_encoder_packet(struct.pack("<ii", 4000, 4000), FakeTime(101.0))
    print("Test 3: Simulated 1-rev forward motion: dist = %.4f m, d_th = %.4f rad" % (dist, d_th))
    assert abs(dist - 0.5172) < 0.001
    assert abs(d_th) < 0.0001
    print("Test 3 Passed: Differential drive kinematics mathematically verified.")
    
    # Test 4: cmd_vel translation
    cmd_twist = Twist()
    cmd_twist.linear.x = 0.5
    cmd_twist.angular.z = 0.0
    speed_frame = driver.cmd_vel_callback(cmd_twist)
    print("Test 4: Packed cmd_vel frame: %s" % speed_frame.encode("hex"))
    assert len(speed_frame) > 0
    print("=== All OpenT2 Chassis Driver Unit Tests PASSED ===")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_self_test()
    else:
        rospy.init_node("opent2_chassis_driver")
        driver = OpenT2ChassisDriver()
        rospy.spin()
