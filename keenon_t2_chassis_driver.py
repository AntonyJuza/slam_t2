#!/usr/bin/env python3
"""
Keenon T2 ROS 2 Native Chassis Driver
=====================================
Direct USB Serial Driver for Keenon T2 Mobile Robot Base (STM32 Controller).
Publishes:
  - /odom (nav_msgs/msg/Odometry)
  - /tf (odom -> base_link)
  - /imu/data_raw (sensor_msgs/msg/Imu)

Subscribes:
  - /cmd_vel (geometry_msgs/msg/Twist)
"""

import math
import struct
import sys
import time

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from tf2_ros import TransformBroadcaster

import serial

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

class KeenonT2ChassisDriver(Node):
    def __init__(self):
        super().__init__('keenon_t2_chassis_driver')

        # Parameters
        self.declare_parameter('port', '/dev/ttyUSB2')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_gauge', 0.366)       # 366 mm track width
        self.declare_parameter('wheel_perimeter', 0.5172)  # 517.2 mm perimeter
        self.declare_parameter('publish_tf', True)
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('imu_frame', 'imu_link')

        self.port_name = self.get_parameter('port').value
        self.baudrate = self.get_parameter('baudrate').value
        self.wheel_gauge = self.get_parameter('wheel_gauge').value
        self.wheel_perimeter = self.get_parameter('wheel_perimeter').value
        self.publish_tf = self.get_parameter('publish_tf').value
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value
        self.imu_frame = self.get_parameter('imu_frame').value

        # Open Serial Port
        self.get_logger().info(f"Opening serial port {self.port_name} at {self.baudrate} baud...")
        self.ser = serial.Serial(self.port_name, self.baudrate, timeout=0.02)
        self.get_logger().info(f"Successfully connected to Keenon T2 chassis!")

        # Publishers & Broadcasters
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data_raw', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscriber
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # Internal State
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.prev_left_ticks = None
        self.prev_right_ticks = None
        self.last_telemetry_time = self.get_clock().now()

        # Command velocity variables
        self.target_linear_x = 0.0
        self.target_angular_z = 0.0
        self.last_cmd_time = time.time()

        # Serial read buffer
        self.rx_buffer = bytearray()

        # Timer for main loop (50Hz)
        self.timer = self.create_timer(0.02, self.spin_driver)

    def cmd_vel_callback(self, msg: Twist):
        self.target_linear_x = msg.linear.x
        self.target_angular_z = msg.angular.z
        self.last_cmd_time = time.time()

    def send_motor_command(self, v_m_s: float, w_rad_s: float):
        """Packs motor velocity command into Keenon STM32 UART frame."""
        v_mm_s = int(v_m_s * 1000.0)
        w_mrad_s = int(w_rad_s * 1000.0)

        payload = struct.pack('<ii', v_mm_s, w_mrad_s)
        cmd_id = 0x20
        seq = 0x00
        length = len(payload)

        header = bytes([0xAA, 0xAA, 0x00, 0xE0, cmd_id, seq, length])
        
        checksum_val = sum(header[2:]) + sum(payload)
        crc = struct.pack('<H', checksum_val & 0xFFFF)

        packet = header + payload + crc + TAIL
        try:
            self.ser.write(packet)
        except Exception as e:
            self.get_logger().error(f"Serial write error: {e}")

    def spin_driver(self):
        # 1. Read serial data
        try:
            bytes_to_read = self.ser.in_waiting
            if bytes_to_read > 0:
                chunk = self.ser.read(bytes_to_read)
                self.rx_buffer.extend(chunk)
        except Exception as e:
            self.get_logger().error(f"Serial read error: {e}")
            return

        # 2. Parse telemetry frames
        while True:
            idx = self.rx_buffer.find(HEADER)
            if idx == -1:
                if len(self.rx_buffer) > 1:
                    self.rx_buffer = self.rx_buffer[-1:]
                break

            if idx > 0:
                self.rx_buffer = self.rx_buffer[idx:]

            end_idx = self.rx_buffer.find(TAIL)
            if end_idx == -1:
                break # Wait for complete frame

            frame = self.rx_buffer[:end_idx+2]
            self.rx_buffer = self.rx_buffer[end_idx+2:]

            if len(frame) >= 11:
                cmd_id = frame[4]
                payload_len = frame[6]
                payload = frame[7:7+payload_len]

                if cmd_id == 0x2D and payload_len == 12:
                    self.process_encoder_frame(payload)
                elif cmd_id == 0x32 and payload_len == 16:
                    self.process_imu_frame(payload)

        # 3. Safety Watchdog & Send motor command
        if time.time() - self.last_cmd_time > 0.5:
            self.target_linear_x = 0.0
            self.target_angular_z = 0.0

        self.send_motor_command(self.target_linear_x, self.target_angular_z)

    def process_encoder_frame(self, payload: bytes):
        cur_vel_raw, left_ticks, right_ticks = struct.unpack('<iii', payload)
        now = self.get_clock().now()

        if self.prev_left_ticks is not None:
            dt = (now - self.last_telemetry_time).nanoseconds / 1e9
            if dt > 0.001:
                d_left = left_ticks - self.prev_left_ticks
                d_right = right_ticks - self.prev_right_ticks

                # Encoder scaling: delta tick scaling
                # Note: wheel_perimeter / 65536.0 or encoder resolution
                # If ticks are raw 32-bit counts:
                dist_left = (d_left / 65536.0) * self.wheel_perimeter
                dist_right = (d_right / 65536.0) * self.wheel_perimeter

                dist_center = (dist_left + dist_right) / 2.0
                delta_theta = (dist_right - dist_left) / self.wheel_gauge

                # Pose Integration (Standard ROS ENU)
                self.x += dist_center * math.cos(self.theta + delta_theta / 2.0)
                self.y += dist_center * math.sin(self.theta + delta_theta / 2.0)
                self.theta += delta_theta

                v_x = dist_center / dt
                v_theta = delta_theta / dt

                self.publish_odometry(now, v_x, v_theta)

        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks
        self.last_telemetry_time = now

    def publish_odometry(self, now, v_x, v_theta):
        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = v_x
        odom.twist.twist.angular.z = v_theta

        self.odom_pub.publish(odom)

        if self.publish_tf:
            t = TransformStamped()
            t.header.stamp = now.to_msg()
            t.header.frame_id = self.odom_frame
            t.child_frame_id = self.base_frame

            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0
            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = qz
            t.transform.rotation.w = qw

            self.tf_broadcaster.sendTransform(t)

    def process_imu_frame(self, payload: bytes):
        ax, ay, az, gz = struct.unpack('<ffff', payload)
        now = self.get_clock().now()

        imu = Imu()
        imu.header.stamp = now.to_msg()
        imu.header.frame_id = self.imu_frame

        imu.linear_acceleration.x = float(ax)
        imu.linear_acceleration.y = float(ay)
        imu.linear_acceleration.z = float(az)

        imu.angular_velocity.z = float(gz)

        self.imu_pub.publish(imu)

def main(args=None):
    rclpy.init(args=args)
    driver_node = KeenonT2ChassisDriver()
    try:
        rclpy.spin(driver_node)
    except KeyboardInterrupt:
        pass
    finally:
        driver_node.send_motor_command(0.0, 0.0)
        driver_node.ser.close()
        driver_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
