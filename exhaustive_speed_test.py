#!/usr/bin/env python3
"""
Try EVERY possible speed command payload format.
The STM32 ACKs our CMD 0x20, but velocity stays 0.
Maybe the payload format is different from what we assume.
"""
import serial
import struct
import time

PORT = '/dev/ttyUSB2'
BAUD = 115200

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

def check_movement(ser, duration=0.8):
    """Returns True if velocity field in 0x2D becomes nonzero."""
    buf = bytearray()
    start = time.time()
    while time.time() - start < duration:
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
        while True:
            idx = buf.find(b'\xAA\xAA')
            if idx == -1: break
            end = buf.find(b'\x55\x55', idx+2)
            if end == -1: break
            frame = buf[idx:end+2]
            buf = buf[end+2:]
            if len(frame) >= 11 and frame[4] == 0x2D and frame[6] == 12:
                vel = struct.unpack('<i', frame[7:11])[0]
                if vel != 0:
                    return True, vel
        time.sleep(0.01)
    return False, 0

ser = serial.Serial(PORT, BAUD, timeout=0.05)
ser.reset_input_buffer()

print("=" * 60)
print("  EXHAUSTIVE SPEED PAYLOAD FORMAT TEST")
print("=" * 60)

# Always unlock first
ser.write(build_pkt(0x21, b'\x01'))
time.sleep(0.1)

# Test formats
test_payloads = [
    # (label, payload_bytes)
    # 4-byte formats
    ("int16 LE (v=200, w=0)",           struct.pack('<hh', 200, 0)),
    ("int16 BE (v=200, w=0)",           struct.pack('>hh', 200, 0)),
    ("uint16 LE (v=200, w=0)",          struct.pack('<HH', 200, 0)),
    ("int16 LE (v=1000, w=0)",          struct.pack('<hh', 1000, 0)),
    ("int16 LE (v=100, w=0)",           struct.pack('<hh', 100, 0)),
    ("int16 LE (v=50, w=0)",            struct.pack('<hh', 50, 0)),
    
    # 8-byte formats
    ("int32 LE (v=200, w=0)",           struct.pack('<ii', 200, 0)),
    ("int32 LE (v=1000, w=0)",          struct.pack('<ii', 1000, 0)),
    ("float32 LE (v=0.2, w=0)",         struct.pack('<ff', 0.2, 0.0)),
    ("float32 LE (v=200, w=0)",         struct.pack('<ff', 200.0, 0.0)),
    
    # 2-byte format (just linear)
    ("int16 LE v=200 only",             struct.pack('<h', 200)),
    ("int16 LE v=1000 only",            struct.pack('<h', 1000)),
    
    # 6-byte format (int16 left_vel, int16 right_vel, int16 ???)
    ("3x int16 (L=200, R=200, 0)",      struct.pack('<hhh', 200, 200, 0)),
    
    # Left/Right wheel velocities instead of v/w
    ("int16 left=200, right=200",       struct.pack('<hh', 200, 200)),
    ("int16 left=500, right=500",       struct.pack('<hh', 500, 500)),
    ("int32 left=200, right=200",       struct.pack('<ii', 200, 200)),
    
    # Raw byte patterns
    ("raw: C8 00 00 00",               b'\xC8\x00\x00\x00'),
    ("raw: 00 C8 00 00",               b'\x00\xC8\x00\x00'),
    ("raw: 01 00 C8 00",               b'\x01\x00\xC8\x00'),
    ("raw: C8 00 C8 00",               b'\xC8\x00\xC8\x00'),
]

for label, payload in test_payloads:
    ser.reset_input_buffer()
    
    # Send 20 speed frames
    for _ in range(20):
        ser.write(build_pkt(0x20, payload))
        time.sleep(0.02)
    
    moved, vel = check_movement(ser, 0.5)
    status = "MOVED!!!" if moved else "no"
    print(f"  [{status:8s}] {label:45s} hex={payload.hex()}")
    
    # Stop
    ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
    time.sleep(0.1)

# Also try completely different CMD IDs for speed
print("\n--- Testing alternative speed CMD IDs ---")
speed_payload = struct.pack('<hh', 300, 0)
for cmd_id in [0x01, 0x02, 0x03, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x30, 0x33, 0x34, 0x35, 0x40]:
    ser.reset_input_buffer()
    for _ in range(10):
        ser.write(build_pkt(cmd_id, speed_payload))
        time.sleep(0.02)
    
    moved, vel = check_movement(ser, 0.3)
    if moved:
        print(f"  MOVED with CMD 0x{cmd_id:02X}! vel={vel}")

    ser.write(build_pkt(cmd_id, struct.pack('<hh', 0, 0)))
    time.sleep(0.05)

print("\nDone.")
ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()
