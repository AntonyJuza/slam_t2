#!/usr/bin/env python3
"""
Battery & Power State Monitor + Force Motor Test
=================================================
The STM32 reports battery=0%. This is likely the motor interlock.
This script monitors battery state and attempts to override with
different CMD sequences used by the original firmware.
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

ser = serial.Serial(PORT, BAUD, timeout=0.05)
ser.reset_input_buffer()

print("=" * 60)
print("  BATTERY STATE & MOTOR OVERRIDE TEST")
print("=" * 60)

# Read battery state
buf = bytearray()
start = time.time()
battery_samples = []
power_samples = []

while time.time() - start < 2.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    while True:
        idx = buf.find(b'\xAA\xAA')
        if idx == -1: break
        end = buf.find(b'\x55\x55', idx+2)
        if end == -1: break
        frame = buf[idx:end+2]
        buf = buf[end+2:]
        if len(frame) >= 11:
            cmd = frame[4]
            plen = frame[6]
            p = frame[7:7+plen]
            if cmd == 0x2B and plen == 2:
                battery_samples.append((p[0], p[1]))
            elif cmd == 0x2F and plen == 16:
                power_samples.append(p)
    time.sleep(0.01)

print(f"\nBattery 0x2B samples: {len(battery_samples)}")
if battery_samples:
    b = battery_samples[-1]
    print(f"  byte0={b[0]}, byte1={b[1]} (0x{b[1]:02X})")
    print(f"  Interpretation: Battery={b[0]}%, StateFlag=0x{b[1]:02X}")
    if b[0] == 0:
        print("  >>> BATTERY AT 0% - THIS IS LIKELY THE MOTOR INTERLOCK! <<<")

print(f"\nPower 0x2F samples: {len(power_samples)}")
if power_samples:
    p = power_samples[-1]
    # Try byte-level decode
    print(f"  Raw: {p.hex()}")
    # Try as mixed format
    byte0 = p[0]
    byte1 = p[1]
    val1 = struct.unpack('<H', p[0:2])[0]
    val2 = struct.unpack('<H', p[2:4])[0]
    val3 = struct.unpack('<I', p[4:8])[0]
    val4 = struct.unpack('<I', p[8:12])[0]
    val5 = struct.unpack('<I', p[12:16])[0]
    print(f"  uint16[0]={val1} (0x{val1:04X})")
    print(f"  uint16[1]={val2} (0x{val2:04X})")
    print(f"  uint32[2]={val3}")
    print(f"  uint32[3]={val4}")
    print(f"  uint32[4]={val5}")
    
    # Maybe bytes 0-1 are voltage in different scale
    # 0x1000 = 4096 -> 40.96V? or 24.0V?
    # Let's also try individual bytes
    print(f"  All bytes: {' '.join(f'{b:02X}' for b in p)}")

# Now try to send battery override / force motor enable
print("\n--- Attempting Motor Force-Enable Sequences ---")

# Strategy 1: Send fake battery state to STM32
# Original chassis binary likely sent periodic heartbeat/status
for cmd in range(0x20, 0x50):
    # Skip known telemetry CMDs we receive FROM stm32
    if cmd in [0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x31, 0x32, 0x41, 0x20, 0x22]:
        continue
    for pay in [b'\x00', b'\x01', b'\x02', b'\xFF']:
        pkt = build_pkt(cmd, pay)
        ser.write(pkt)
        time.sleep(0.01)

# Wait and check responses
time.sleep(0.5)
buf = bytearray()
start = time.time()
new_cmds = set()
while time.time() - start < 1.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    while True:
        idx = buf.find(b'\xAA\xAA')
        if idx == -1: break
        end = buf.find(b'\x55\x55', idx+2)
        if end == -1: break
        frame = buf[idx:end+2]
        buf = buf[end+2:]
        if len(frame) >= 11:
            cmd = frame[4]
            plen = frame[6]
            p = frame[7:7+plen]
            new_cmds.add(cmd)
            if cmd not in [0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x31, 0x32, 0x41, 0x20, 0x22]:
                print(f"  NEW RESPONSE! CMD 0x{cmd:02X} payload={p.hex()}")
    time.sleep(0.01)

print(f"\n  All response CMDs seen: {[f'0x{c:02X}' for c in sorted(new_cmds)]}")

# Strategy 2: Try motor unlock with CMD 0x21 payload 0x01, then immediately
# send speed with different packet rates
print("\n--- High-frequency speed burst test ---")
ser.reset_input_buffer()
ser.write(build_pkt(0x21, b'\x01'))
time.sleep(0.02)

# Burst 100 speed commands as fast as possible
speed_payload = struct.pack('<hh', 300, 0)
for _ in range(100):
    ser.write(build_pkt(0x20, speed_payload))
    time.sleep(0.005)  # 200 Hz

# Check encoder velocity
buf = bytearray()
start = time.time()
while time.time() - start < 1.0:
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
                print(f"  MOTOR MOVING! vel={vel}")
    time.sleep(0.01)

# Stop
ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()

print("\n" + "=" * 60)
print("  CONCLUSION: If battery=0% and no movement,")
print("  the STM32 low-battery cutoff is blocking motor drive.")
print("  Check: Is robot battery charged? Is BMS connected?")
print("=" * 60)
