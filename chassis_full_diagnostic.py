#!/usr/bin/env python3
"""
Keenon T2 Chassis - Full Diagnostic & Motion Test
==================================================
Tests EVERY combination of header, CRC, unlock, and speed command
to find what actually makes the motors spin.
"""
import serial
import struct
import time
import sys

PORT = '/dev/ttyUSB2'
BAUD = 115200
TAIL = bytes([0x55, 0x55])

def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

def additive_checksum(data: bytes) -> int:
    return sum(data) & 0xFFFF

def build_packet(src, dst, cmd_id, payload, use_modbus_crc=True):
    """Build a complete Keenon serial frame."""
    seq = 0x00
    length = len(payload)
    hdr_bytes = bytes([src, dst, cmd_id, seq, length])
    
    if use_modbus_crc:
        crc_val = crc16_modbus(hdr_bytes + payload)
    else:
        crc_val = additive_checksum(hdr_bytes + payload)
    
    crc_bytes = struct.pack('<H', crc_val)
    return bytes([0xAA, 0xAA]) + hdr_bytes + payload + crc_bytes + TAIL

def parse_frames(buf):
    """Extract all complete frames from buffer."""
    frames = []
    hdr = bytes([0xAA, 0xAA])
    while True:
        idx = buf.find(hdr)
        if idx == -1:
            break
        end = buf.find(TAIL, idx + 2)
        if end == -1:
            break
        frame = buf[idx:end+2]
        buf = buf[end+2:]
        if len(frame) >= 11:
            frames.append(frame)
    return frames, buf

def read_all_frames(ser, duration=1.0):
    """Read serial data for 'duration' seconds and parse all frames."""
    start = time.time()
    buf = bytearray()
    all_frames = []
    while time.time() - start < duration:
        if ser.in_waiting:
            buf.extend(ser.read(ser.in_waiting))
        time.sleep(0.01)
    frames, _ = parse_frames(buf)
    return frames

def decode_frame(frame):
    """Return dict with cmd, payload, etc."""
    return {
        'src': frame[2],
        'dst': frame[3],
        'cmd': frame[4],
        'seq': frame[5],
        'length': frame[6],
        'payload': frame[7:7+frame[6]],
        'raw': frame.hex()
    }

def get_encoder_ticks(frames):
    """Extract encoder ticks from 0x2D frames."""
    for f in frames:
        d = decode_frame(f)
        if d['cmd'] == 0x2D and d['length'] == 12:
            vel, left, right = struct.unpack('<iii', d['payload'])
            return vel, left, right
    return None

# ============================================================
print("=" * 60)
print("  KEENON T2 CHASSIS - FULL DIAGNOSTIC")
print("=" * 60)

ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(0.2)
ser.reset_input_buffer()

# ---- PHASE 1: Read baseline status ----
print("\n[PHASE 1] Reading baseline telemetry (2 seconds)...")
frames = read_all_frames(ser, 2.0)

cmd_summary = {}
for f in frames:
    d = decode_frame(f)
    key = (d['cmd'], d['length'])
    if key not in cmd_summary:
        cmd_summary[key] = []
    cmd_summary[key].append(d['payload'].hex())

print(f"  Received {len(frames)} frames total")
print(f"  Unique CMD types: {len(cmd_summary)}")
for (cmd, length), payloads in sorted(cmd_summary.items()):
    unique_vals = set(payloads)
    print(f"    CMD 0x{cmd:02X} (len={length}): {len(payloads)} frames, values: {unique_vals if len(unique_vals) <= 5 else f'{len(unique_vals)} unique'}")

# Decode specific status bytes
for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2E and d['length'] == 1:
        print(f"\n  >> MOTOR STATUS (0x2E): payload=0x{d['payload'][0]:02X} ({'LOCKED/E-STOP' if d['payload'][0]==0x00 else 'UNLOCKED/READY'})")
        break

for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x41 and d['length'] == 1:
        print(f"  >> STATUS 0x41: payload=0x{d['payload'][0]:02X}")
        break

for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2C and d['length'] == 1:
        print(f"  >> STATUS 0x2C: payload=0x{d['payload'][0]:02X}")
        break

for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2A and d['length'] == 1:
        print(f"  >> STATUS 0x2A: payload=0x{d['payload'][0]:02X}")
        break

enc = get_encoder_ticks(frames)
if enc:
    print(f"  >> ENCODER (0x2D): vel={enc[0]}, left_ticks={enc[1]}, right_ticks={enc[2]}")

# Decode battery (0x2B)
for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2B and d['length'] == 2:
        batt_raw = struct.unpack('<H', d['payload'])[0]
        print(f"  >> BATTERY (0x2B): raw={batt_raw} ({batt_raw/10.0 if batt_raw < 1000 else batt_raw}%)")
        break

# Decode 0x2F (power/voltage?)
for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2F and d['length'] == 16:
        vals = struct.unpack('<IIII', d['payload'])
        print(f"  >> POWER (0x2F): {[hex(v) for v in vals]}")
        break

# ---- PHASE 2: Try ALL unlock + speed combinations ----
print("\n[PHASE 2] Testing motor unlock + speed command combinations...")

test_combos = [
    # (label, src, dst, unlock_cmd, unlock_payload, speed_cmd, use_modbus)
    ("Header E0->00, CRC16-Modbus, unlock=0x01",   0xE0, 0x00, 0x21, b'\x01', True),
    ("Header E0->00, CRC16-Modbus, unlock=0x00",   0xE0, 0x00, 0x21, b'\x00', True),
    ("Header 00->E0, CRC16-Modbus, unlock=0x01",   0x00, 0xE0, 0x21, b'\x01', True),
    ("Header 00->E0, CRC16-Modbus, unlock=0x00",   0x00, 0xE0, 0x21, b'\x00', True),
    ("Header E0->00, Additive CRC, unlock=0x01",    0xE0, 0x00, 0x21, b'\x01', False),
    ("Header 00->E0, Additive CRC, unlock=0x01",    0x00, 0xE0, 0x21, b'\x01', False),
    ("Header 00->E0, Additive CRC, unlock=0x00",    0x00, 0xE0, 0x21, b'\x00', False),
]

speed_payload = struct.pack('<hh', 200, 0)  # 200 mm/s forward

for label, src, dst, ucmd, upay, use_modbus in test_combos:
    ser.reset_input_buffer()
    
    # Send unlock
    unlock_pkt = build_packet(src, dst, ucmd, upay, use_modbus)
    ser.write(unlock_pkt)
    time.sleep(0.05)
    
    # Send 15 speed frames rapidly
    for _ in range(15):
        spd_pkt = build_packet(src, dst, 0x20, speed_payload, use_modbus)
        ser.write(spd_pkt)
        time.sleep(0.03)
    
    # Read responses for 0.5 sec
    frames = read_all_frames(ser, 0.5)
    
    # Check for encoder movement
    enc_before = None
    enc_after = None
    ack_frames = []
    status_2e = []
    
    for f in frames:
        d = decode_frame(f)
        if d['cmd'] == 0x2D and d['length'] == 12:
            vel, left, right = struct.unpack('<iii', d['payload'])
            if enc_before is None:
                enc_before = (vel, left, right)
            enc_after = (vel, left, right)
        elif d['cmd'] == 0x22:
            ack_frames.append(d['payload'].hex())
        elif d['cmd'] == 0x2E and d['length'] == 1:
            status_2e.append(d['payload'][0])
    
    moved = "NO"
    if enc_before and enc_after:
        if enc_after[0] != 0 or enc_before[1] != enc_after[1]:
            moved = "YES!!!"
    
    status_str = f"0x2E={set(status_2e)}" if status_2e else "no 0x2E"
    ack_str = f"ACKs(0x22)={ack_frames}" if ack_frames else "no ACK"
    
    print(f"  [{moved:6s}] {label}")
    print(f"           {status_str}, {ack_str}")
    
    # Send stop
    stop_pkt = build_packet(src, dst, 0x20, struct.pack('<hh', 0, 0), use_modbus)
    ser.write(stop_pkt)
    time.sleep(0.2)

# ---- PHASE 3: Try 8-byte payload (int32, int32) ----
print("\n[PHASE 3] Testing 8-byte payload (int32 linear, int32 angular)...")
for src, dst, use_modbus in [(0xE0, 0x00, True), (0x00, 0xE0, True), (0x00, 0xE0, False)]:
    ser.reset_input_buffer()
    
    # Unlock
    ser.write(build_packet(src, dst, 0x21, b'\x01', use_modbus))
    time.sleep(0.05)
    
    # 8-byte speed: int32 v_mm_s, int32 w_mrad_s
    speed_8 = struct.pack('<ii', 200, 0)
    for _ in range(15):
        ser.write(build_packet(src, dst, 0x20, speed_8, use_modbus))
        time.sleep(0.03)
    
    frames = read_all_frames(ser, 0.5)
    enc_vals = []
    acks = []
    for f in frames:
        d = decode_frame(f)
        if d['cmd'] == 0x2D and d['length'] == 12:
            v, l, r = struct.unpack('<iii', d['payload'])
            enc_vals.append(v)
        elif d['cmd'] == 0x22:
            acks.append(d['payload'].hex())
    
    moved = "YES!!!" if any(v != 0 for v in enc_vals) else "NO"
    hdr_str = f"src=0x{src:02X}->dst=0x{dst:02X}, {'modbus' if use_modbus else 'additive'}"
    print(f"  [{moved:6s}] 8-byte payload, {hdr_str}, ACKs={acks if acks else 'none'}")
    
    ser.write(build_packet(src, dst, 0x20, struct.pack('<ii', 0, 0), use_modbus))
    time.sleep(0.2)

# ---- PHASE 4: Try urgency_stop disable ----
print("\n[PHASE 4] Trying to disable urgency/e-stop via different CMDs...")
# Try sending enable_urgency_button = false equivalent
for cmd_try in [0x41, 0x2C, 0x2A, 0x2E, 0x28, 0x29, 0x23, 0x24, 0x25, 0x26, 0x27]:
    for pay in [b'\x00', b'\x01', b'\x02']:
        for src, dst in [(0xE0, 0x00), (0x00, 0xE0)]:
            pkt = build_packet(src, dst, cmd_try, pay, True)
            ser.write(pkt)
            time.sleep(0.02)

# After sending all override attempts, try speed again
time.sleep(0.1)
ser.reset_input_buffer()
ser.write(build_packet(0xE0, 0x00, 0x21, b'\x01', True))
time.sleep(0.05)

for _ in range(20):
    ser.write(build_packet(0xE0, 0x00, 0x20, struct.pack('<hh', 200, 0), True))
    time.sleep(0.03)

frames = read_all_frames(ser, 0.5)
enc_vals = []
status_2e_vals = []
for f in frames:
    d = decode_frame(f)
    if d['cmd'] == 0x2D and d['length'] == 12:
        v, l, r = struct.unpack('<iii', d['payload'])
        enc_vals.append(v)
    elif d['cmd'] == 0x2E and d['length'] == 1:
        status_2e_vals.append(d['payload'][0])

moved = "YES!!!" if any(v != 0 for v in enc_vals) else "NO"
print(f"  After override attempts: moved={moved}, 0x2E={set(status_2e_vals)}")

# Stop
ser.write(build_packet(0xE0, 0x00, 0x20, struct.pack('<hh', 0, 0), True))

# ---- PHASE 5: Raw dump of ALL unique CMD responses to speed test ----
print("\n[PHASE 5] Capturing ALL responses during speed command burst...")
ser.reset_input_buffer()

# Rapid burst of 50 speed frames
for _ in range(50):
    ser.write(build_packet(0xE0, 0x00, 0x20, struct.pack('<hh', 300, 0), True))
    time.sleep(0.02)

frames = read_all_frames(ser, 1.0)
print(f"  Got {len(frames)} response frames:")
resp_cmds = {}
for f in frames:
    d = decode_frame(f)
    cmd = d['cmd']
    if cmd not in resp_cmds:
        resp_cmds[cmd] = []
    resp_cmds[cmd].append(d['payload'].hex())

for cmd in sorted(resp_cmds.keys()):
    payloads = resp_cmds[cmd]
    unique = set(payloads)
    print(f"    CMD 0x{cmd:02X}: {len(payloads)} frames, unique payloads: {unique if len(unique) <= 5 else f'{len(unique)} unique values'}")

# Final stop
ser.write(build_packet(0xE0, 0x00, 0x20, struct.pack('<hh', 0, 0), True))
ser.close()

print("\n" + "=" * 60)
print("  DIAGNOSTIC COMPLETE")
print("=" * 60)
