#!/usr/bin/env python3
"""
Listen for what the STM32 sends us WITHOUT us sending anything.
Focus on CMD 0x20 and 0x22 which appear even at idle.
Also try to replicate what the original chassis binary would send
as a heartbeat/watchdog.
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
print("  STM32 UNSOLICITED FRAME ANALYSIS")
print("=" * 60)

# Phase 1: Pure listen - no commands sent
print("\n[1] Listening to STM32 for 3 seconds (no commands sent)...")
buf = bytearray()
start = time.time()
all_frames = []

while time.time() - start < 3.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    while True:
        idx = buf.find(b'\xAA\xAA')
        if idx == -1: break
        end = buf.find(b'\x55\x55', idx+2)
        if end == -1: break
        frame = buf[idx:end+2]
        buf = buf[end+2:]
        if len(frame) >= 9:
            cmd = frame[4]
            plen = frame[6]
            p = frame[7:7+plen]
            all_frames.append((time.time()-start, cmd, plen, p, frame))
    time.sleep(0.01)

# Show frame timing for CMD 0x20 and 0x22
print(f"\n  Total frames: {len(all_frames)}")
for t, cmd, plen, p, raw in all_frames:
    if cmd in [0x20, 0x22]:
        print(f"  t={t:5.3f}s CMD 0x{cmd:02X} len={plen} payload={p.hex()} raw={raw.hex()}")

# Show FULL raw hex of a few 0x20 frames
print("\n  Full 0x20 frame examples:")
count = 0
for t, cmd, plen, p, raw in all_frames:
    if cmd == 0x20 and count < 5:
        print(f"    {raw.hex()}")
        # Verify CRC
        data_for_crc = raw[2:7+plen]
        expected_crc = crc16_modbus(data_for_crc)
        actual_crc = struct.unpack('<H', raw[7+plen:9+plen])[0]
        print(f"    CRC check: calculated=0x{expected_crc:04X}, in_frame=0x{actual_crc:04X}, match={expected_crc==actual_crc}")
        count += 1

# Phase 2: The STM32 sends CMD 0x20 to US - maybe it expects us to
# RESPOND to that CMD with the same structure?
print("\n[2] Testing: Echo back CMD 0x20 with speed payload...")
ser.reset_input_buffer()

# Build response to STM32's CMD 0x20 query
# Maybe STM32 sends 0x20 as "give me velocity" and we respond with velocity
for _ in range(50):
    # When STM32 asks via CMD 0x20, we respond with velocity
    ser.write(build_pkt(0x20, struct.pack('<hh', 300, 0)))
    time.sleep(0.02)

# Check
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
                print(f"  VELOCITY NONZERO! vel={vel}")
    time.sleep(0.01)

# Phase 3: Maybe we need to send heartbeat via CMD 0x31 
# (STM32 sends 0x31 with all zeros - maybe we need to respond to it)
print("\n[3] Testing: Respond to STM32 CMD 0x31 heartbeat...")
ser.reset_input_buffer()

# Send CMD 0x31 heartbeat + speed
for _ in range(50):
    ser.write(build_pkt(0x31, struct.pack('<ii', 0, 0)))  # heartbeat
    ser.write(build_pkt(0x21, b'\x01'))  # unlock
    ser.write(build_pkt(0x20, struct.pack('<hh', 300, 0)))  # speed
    time.sleep(0.02)

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
                print(f"  VELOCITY NONZERO! vel={vel}")
    time.sleep(0.01)

# Phase 4: Try CMD 0x21 with different payload values
print("\n[4] Testing CMD 0x21 with various payloads...")
for pay_val in [0x00, 0x01, 0x02, 0x03, 0x04, 0xFF, 0x10, 0x20, 0x40, 0x80]:
    ser.reset_input_buffer()
    ser.write(build_pkt(0x21, bytes([pay_val])))
    time.sleep(0.05)
    
    # Send speed
    for _ in range(20):
        ser.write(build_pkt(0x20, struct.pack('<hh', 300, 0)))
        time.sleep(0.02)
    
    buf = bytearray()
    start = time.time()
    moved = False
    while time.time() - start < 0.5:
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
                    moved = True
        time.sleep(0.01)
    
    print(f"  0x21 payload=0x{pay_val:02X}: {'MOVED!' if moved else 'no movement'}")

    ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
    time.sleep(0.05)

ser.close()
print("\nDone.")
