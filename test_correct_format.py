#!/usr/bin/env python3
"""
CORRECTED frame format: seq is uint16 (2 bytes), not 1 byte!
Frame: AA AA [src] [dst] [cmd] [seq_lo] [seq_hi] [len] [payload...] [crc16_lo] [crc16_hi] 55 55
CRC: CRC16-Modbus over bytes from src through end of payload
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

# Verify against known frames first
print("=== VERIFYING CORRECTED FRAME FORMAT ===\n")

# CMD 0x20 from STM32: aaaa 00e020000100 39  1d75  5555
# Data for CRC: 00 E0 20 00 01 00 39
frame1_data = bytes.fromhex("00E020000100") + bytes([0x39])  
frame1_crc = crc16_modbus(frame1_data)
print(f"CMD 0x20 frame:")
print(f"  Data: {frame1_data.hex()}")
print(f"  Calculated CRC: 0x{frame1_crc:04X}")
print(f"  Expected CRC:   0x751D")
print(f"  Match: {frame1_crc == 0x751D} ✓" if frame1_crc == 0x751D else f"  MISMATCH!")

# Reparse: src=0x00, dst=0xE0, cmd=0x20, seq=0x0000, len=0x01, payload=0x39
print(f"  Parsed: src=0x00, dst=0xE0, cmd=0x20, seq=0x0000, len=1, payload=0x39")

# CMD 0x22 from STM32: aaaa 00e2220001003164 91  5555
# Wait - let me re-examine: aaaa00e2220001003164915555
# If seq is 2 bytes: 00 E2 22 00 01 00 31 64 -> data, 91 xx -> but only 1 CRC byte left?
# Total: 13 bytes = 2(hdr) + ? + 2(crc) + 2(tail) = 7 data bytes
# aaaa [00 E2 22 00 01 00 31] [64 91] 5555
frame2_data = bytes.fromhex("00E22200010031")
frame2_crc = crc16_modbus(frame2_data)
frame2_expected = struct.unpack('<H', bytes.fromhex("6491"))[0]
print(f"\nCMD 0x22 frame:")
print(f"  Data: {frame2_data.hex()}")
print(f"  Calculated CRC: 0x{frame2_crc:04X}")
print(f"  Expected CRC:   0x{frame2_expected:04X}")
print(f"  Match: {frame2_crc == frame2_expected}")

# If match: src=0x00, dst=0xE2, cmd=0x22, seq=0x0000, len=0x01, payload=0x31
if frame2_crc == frame2_expected:
    print(f"  Parsed: src=0x00, dst=0xE2, cmd=0x22, seq=0x0000, len=1, payload=0x31")

# Now let's verify with a longer frame (encoder 0x2D with 12 bytes payload)
# We need to capture a raw frame to verify
print("\n\n=== NOW TESTING CORRECTED PACKET FORMAT ===\n")

def build_correct_pkt(src, dst, cmd_id, seq, payload):
    """Build packet with CORRECTED format: 2-byte seq."""
    length = len(payload)
    data = bytes([src, dst, cmd_id]) + struct.pack('<H', seq) + bytes([length]) + payload
    crc = struct.pack('<H', crc16_modbus(data))
    return b'\xAA\xAA' + data + crc + b'\x55\x55'

ser = serial.Serial(PORT, BAUD, timeout=0.05)
ser.reset_input_buffer()

# First capture a raw encoder frame to verify our parsing
print("[1] Capturing raw 0x2D frame to verify format...")
buf = bytearray()
start = time.time()
while time.time() - start < 1.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    time.sleep(0.01)

# Find 0x2D frames in raw data
raw = bytes(buf)
pos = 0
while pos < len(raw) - 10:
    if raw[pos] == 0xAA and raw[pos+1] == 0xAA:
        # Find next 55 55
        for end in range(pos+8, min(pos+50, len(raw)-1)):
            if raw[end] == 0x55 and raw[end+1] == 0x55:
                frame = raw[pos:end+2]
                if frame[4] == 0x2D:  # CMD
                    print(f"  Raw 0x2D frame: {frame.hex()}")
                    print(f"  Length: {len(frame)} bytes")
                    
                    # With corrected format:
                    # Header(2) + src(1) + dst(1) + cmd(1) + seq(2) + len(1) + payload(len) + crc(2) + tail(2)
                    frame_src = frame[2]
                    frame_dst = frame[3] 
                    frame_cmd = frame[4]
                    frame_seq = struct.unpack('<H', frame[5:7])[0]
                    frame_len = frame[7]
                    frame_payload = frame[8:8+frame_len]
                    frame_crc = frame[8+frame_len:10+frame_len]
                    frame_tail = frame[10+frame_len:]
                    
                    print(f"  src=0x{frame_src:02X}, dst=0x{frame_dst:02X}, cmd=0x{frame_cmd:02X}")
                    print(f"  seq={frame_seq}, len={frame_len}")
                    print(f"  payload={frame_payload.hex()}")
                    print(f"  crc={frame_crc.hex()}")
                    print(f"  tail={frame_tail.hex()}")
                    
                    # Verify CRC
                    data_for_crc = frame[2:8+frame_len]
                    calc_crc = crc16_modbus(data_for_crc)
                    actual_crc = struct.unpack('<H', frame_crc)[0]
                    print(f"  CRC verify: calc=0x{calc_crc:04X}, actual=0x{actual_crc:04X}, match={calc_crc==actual_crc}")
                    
                    if frame_len == 12:
                        vel, left, right = struct.unpack('<iii', frame_payload)
                        print(f"  Encoder: vel={vel}, L={left}, R={right}")
                    
                    break
                break
    pos += 1

# [2] NOW send speed commands with CORRECT format
print("\n[2] Sending speed commands with CORRECTED frame format...")
ser.reset_input_buffer()

seq_counter = 0

# Send unlock
pkt = build_correct_pkt(0xE0, 0x00, 0x21, seq_counter, b'\x01')
print(f"  Unlock packet: {pkt.hex()}")
ser.write(pkt)
seq_counter += 1
time.sleep(0.1)

# Send speed (200 mm/s forward) - 4 byte payload: int16 v, int16 w
speed_payload = struct.pack('<hh', 200, 0)
print(f"\n  Sending 30 speed frames at 200mm/s...")
for i in range(30):
    pkt = build_correct_pkt(0xE0, 0x00, 0x20, seq_counter, speed_payload)
    ser.write(pkt)
    seq_counter += 1
    time.sleep(0.03)

# Check for movement
buf = bytearray()
start = time.time()
velocities = []
while time.time() - start < 1.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    while True:
        idx = buf.find(b'\xAA\xAA')
        if idx == -1: break
        end_idx = buf.find(b'\x55\x55', idx+2)
        if end_idx == -1: break
        frame = buf[idx:end_idx+2]
        buf = buf[end_idx+2:]
        if len(frame) >= 14 and frame[4] == 0x2D:
            flen = frame[7]
            if flen == 12:
                vel = struct.unpack('<i', frame[8:12])[0]
                velocities.append(vel)
    time.sleep(0.01)

print(f"  Velocity samples: {len(velocities)}")
if velocities:
    unique_vels = set(velocities)
    print(f"  Unique velocities: {unique_vels}")
    if any(v != 0 for v in velocities):
        print("  >>> MOTOR IS MOVING! <<<")
    else:
        print("  Still velocity=0 :(")

# Stop
ser.write(build_correct_pkt(0xE0, 0x00, 0x20, seq_counter, struct.pack('<hh', 0, 0)))
ser.close()
print("\nDone.")
