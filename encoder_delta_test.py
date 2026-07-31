#!/usr/bin/env python3
"""
Check if encoder ticks ACTUALLY change when we send speed commands.
Compare encoder deltas during idle vs. during speed commands.
"""
import serial
import struct
import time

PORT = '/dev/ttyUSB2'
BAUD = 115200
TAIL = bytes([0x55, 0x55])

def crc16_modbus(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

def build_pkt(cmd_id, payload):
    hdr = bytes([0xE0, 0x00, cmd_id, 0x00, len(payload)])
    crc = struct.pack('<H', crc16_modbus(hdr + payload))
    return b'\xAA\xAA' + hdr + payload + crc + b'\x55\x55'

def get_encoder_samples(ser, duration, send_speed=False, speed_mm_s=0):
    """Collect encoder tick samples over 'duration' seconds."""
    start = time.time()
    buf = bytearray()
    samples = []
    
    while time.time() - start < duration:
        if send_speed and speed_mm_s != 0:
            ser.write(build_pkt(0x20, struct.pack('<hh', speed_mm_s, 0)))
        
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
        
        # Parse frames
        hdr = b'\xAA\xAA'
        while True:
            idx = buf.find(hdr)
            if idx == -1: break
            end = buf.find(TAIL, idx+2)
            if end == -1: break
            frame = buf[idx:end+2]
            buf = buf[end+2:]
            if len(frame) >= 11 and frame[4] == 0x2D and frame[6] == 12:
                payload = frame[7:19]
                vel, left, right = struct.unpack('<iii', payload)
                samples.append((time.time() - start, vel, left, right))
        
        time.sleep(0.02)
    
    return samples

ser = serial.Serial(PORT, BAUD, timeout=0.05)
ser.reset_input_buffer()

print("=" * 60)
print("  ENCODER DELTA TEST")
print("=" * 60)

# Phase A: idle (no commands)
print("\n[A] IDLE - No commands (2 sec)...")
idle_samples = get_encoder_samples(ser, 2.0)
if len(idle_samples) >= 2:
    d_left = idle_samples[-1][2] - idle_samples[0][2]
    d_right = idle_samples[-1][3] - idle_samples[0][3]
    print(f"   Samples: {len(idle_samples)}")
    print(f"   First: vel={idle_samples[0][1]}, L={idle_samples[0][2]}, R={idle_samples[0][3]}")
    print(f"   Last:  vel={idle_samples[-1][1]}, L={idle_samples[-1][2]}, R={idle_samples[-1][3]}")
    print(f"   Delta: dL={d_left}, dR={d_right}")

# Phase B: sending unlock + speed
print("\n[B] SPEED - Sending unlock + 200mm/s forward (2 sec)...")
ser.write(build_pkt(0x21, b'\x01'))
time.sleep(0.05)
speed_samples = get_encoder_samples(ser, 2.0, send_speed=True, speed_mm_s=200)
if len(speed_samples) >= 2:
    d_left = speed_samples[-1][2] - speed_samples[0][2]
    d_right = speed_samples[-1][3] - speed_samples[0][3]
    print(f"   Samples: {len(speed_samples)}")
    print(f"   First: vel={speed_samples[0][1]}, L={speed_samples[0][2]}, R={speed_samples[0][3]}")
    print(f"   Last:  vel={speed_samples[-1][1]}, L={speed_samples[-1][2]}, R={speed_samples[-1][3]}")
    print(f"   Delta: dL={d_left}, dR={d_right}")
    
    # Check vel field
    vels = [s[1] for s in speed_samples]
    unique_vels = set(vels)
    print(f"   Velocity field values: {unique_vels}")

# Phase C: high speed test
print("\n[C] HIGH SPEED - 500mm/s forward (2 sec)...")
ser.write(build_pkt(0x21, b'\x01'))
time.sleep(0.05)
fast_samples = get_encoder_samples(ser, 2.0, send_speed=True, speed_mm_s=500)
if len(fast_samples) >= 2:
    d_left = fast_samples[-1][2] - fast_samples[0][2]
    d_right = fast_samples[-1][3] - fast_samples[0][3]
    print(f"   Samples: {len(fast_samples)}")
    print(f"   First: vel={fast_samples[0][1]}, L={fast_samples[0][2]}, R={fast_samples[0][3]}")
    print(f"   Last:  vel={fast_samples[-1][1]}, L={fast_samples[-1][2]}, R={fast_samples[-1][3]}")
    print(f"   Delta: dL={d_left}, dR={d_right}")
    
    vels = [s[1] for s in fast_samples]
    unique_vels = set(vels)
    print(f"   Velocity field values: {unique_vels}")

# Stop
ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()

print("\n" + "=" * 60)
print("  If Delta dL/dR are similar in idle vs speed,")
print("  encoders are just incrementing on their own (timestamp-based)")
print("  and the motor is NOT actually spinning.")
print("=" * 60)
