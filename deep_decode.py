#!/usr/bin/env python3
"""
Deep decode all telemetry frames to find the interlock condition.
"""
import serial
import struct
import time

PORT = '/dev/ttyUSB2'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=0.05)
ser.reset_input_buffer()

print("=" * 60)
print("  DEEP TELEMETRY DECODE")
print("=" * 60)

buf = bytearray()
start = time.time()
frames_by_cmd = {}

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
        if len(frame) >= 11:
            cmd = frame[4]
            plen = frame[6]
            payload = frame[7:7+plen]
            if cmd not in frames_by_cmd:
                frames_by_cmd[cmd] = []
            frames_by_cmd[cmd].append(payload)
    time.sleep(0.01)

ser.close()

# Decode each CMD type
for cmd in sorted(frames_by_cmd.keys()):
    payloads = frames_by_cmd[cmd]
    p = payloads[-1]  # Use last sample
    
    print(f"\nCMD 0x{cmd:02X} ({len(payloads)} frames, payload_len={len(p)}):")
    print(f"  Raw hex: {p.hex()}")
    
    if cmd == 0x2D and len(p) == 12:
        v1, v2, v3 = struct.unpack('<iii', p)
        # Try as uint32
        u1, u2, u3 = struct.unpack('<III', p)
        print(f"  As int32:  [{v1}, {v2}, {v3}]")
        print(f"  As uint32: [{u1}, {u2}, {u3}]")
        # Try as int16 pairs
        s1, s2, s3, s4, s5, s6 = struct.unpack('<hhhhhh', p)
        print(f"  As int16:  [{s1}, {s2}, {s3}, {s4}, {s5}, {s6}]")
    
    elif cmd == 0x32 and len(p) == 16:
        # Try as 4 floats
        f1, f2, f3, f4 = struct.unpack('<ffff', p)
        print(f"  As float32: [{f1:.6f}, {f2:.6f}, {f3:.6f}, {f4:.6f}]")
        # First byte then 3 floats + padding?
        print(f"  Byte[0]=0x{p[0]:02X}, remaining as 3 floats + byte: ", end="")
        if len(p) >= 13:
            fa, fb, fc = struct.unpack('<fff', p[1:13])
            print(f"[{fa:.6f}, {fb:.6f}, {fc:.6f}], tail={p[13:].hex()}")
    
    elif cmd == 0x2F and len(p) == 16:
        # Try multiple interpretations
        u1, u2, u3, u4 = struct.unpack('<IIII', p)
        print(f"  As uint32: [{u1}, {u2}, {u3}, {u4}]")
        s1, s2, s3, s4, s5, s6, s7, s8 = struct.unpack('<HHHHHHHH', p)
        print(f"  As uint16: [{s1}, {s2}, {s3}, {s4}, {s5}, {s6}, {s7}, {s8}]")
        # Voltage interpretation
        print(f"  Possible voltage: {s1/100.0}V or {s1/10.0}V")
        print(f"  Possible current: {s2} mA or {s3} mA")
        # Try byte by byte
        print(f"  Bytes: {[f'0x{b:02X}' for b in p]}")
    
    elif cmd == 0x2B and len(p) == 2:
        val = struct.unpack('<H', p)[0]
        print(f"  As uint16: {val}")
        print(f"  As battery %: {val / 100.0}% or {val / 256.0}%")
        # First byte could be percentage, second byte could be flags
        print(f"  Byte[0]={p[0]} (battery?), Byte[1]={p[1]} (flags?)")
    
    elif cmd == 0x31 and len(p) == 8:
        v1, v2 = struct.unpack('<ii', p)
        print(f"  As int32: [{v1}, {v2}]")
        f1, f2 = struct.unpack('<ff', p)
        print(f"  As float32: [{f1}, {f2}]")
    
    elif len(p) == 1:
        print(f"  Value: {p[0]} (0x{p[0]:02X})")
        # For status bytes, show bit interpretation
        bits = f'{p[0]:08b}'
        print(f"  Bits: {bits}")
    
    else:
        # Generic decode
        if len(p) <= 4:
            vals = struct.unpack(f'<{"B" * len(p)}', p)
            print(f"  As bytes: {[f'0x{v:02X}' for v in vals]}")

# Additional: decode battery byte properly
print("\n--- Battery / Charging Analysis ---")
if 0x2B in frames_by_cmd:
    p = frames_by_cmd[0x2B][-1]
    print(f"  0x2B: byte0={p[0]}, byte1={p[1]}")
    print(f"  If byte0=percentage: {p[0]}%")
    print(f"  If byte1=0x{p[1]:02X} is charging state: {'CHARGING' if p[1] else 'NOT CHARGING'}")

if 0x2F in frames_by_cmd:
    p = frames_by_cmd[0x2F][-1]
    vals = struct.unpack('<HHHHHHHH', p)
    print(f"\n  0x2F detail:")
    print(f"    Field 0: {vals[0]} (0x{vals[0]:04X}) - maybe status/error code?")
    print(f"    Field 1: {vals[1]} (0x{vals[1]:04X}) - maybe voltage*10?  = {vals[1]/10.0}V")
    print(f"    Field 2: {vals[2]} (0x{vals[2]:04X})")
    print(f"    Field 3: {vals[3]} (0x{vals[3]:04X}) - maybe current?")
    print(f"    Field 4: {vals[4]} (0x{vals[4]:04X})")
    print(f"    Field 5: {vals[5]} (0x{vals[5]:04X})")
    print(f"    Field 6: {vals[6]} (0x{vals[6]:04X})")
    print(f"    Field 7: {vals[7]} (0x{vals[7]:04X})")

# Check if robot is on charger
if 0x2C in frames_by_cmd:
    p = frames_by_cmd[0x2C][-1]
    print(f"\n  0x2C (charge_state?): {p[0]} (0x{p[0]:02X})")
    print(f"    {'ON CHARGER' if p[0] else 'OFF CHARGER'}")

if 0x41 in frames_by_cmd:
    p = frames_by_cmd[0x41][-1]
    print(f"\n  0x41 (urgency_button?): {p[0]} (0x{p[0]:02X})")
    print(f"    {'E-STOP PRESSED' if p[0] else 'E-STOP RELEASED'}")

if 0x2A in frames_by_cmd:
    p = frames_by_cmd[0x2A][-1]
    print(f"\n  0x2A (bumper?): {p[0]} (0x{p[0]:02X})")

if 0x2E in frames_by_cmd:
    p = frames_by_cmd[0x2E][-1]
    print(f"\n  0x2E (motor_lock_status): {p[0]} (0x{p[0]:02X})")
    print(f"    If 0=unlocked: MOTORS UNLOCKED (ready)")
    print(f"    If 0=locked:   MOTORS LOCKED (interlock)")

if 0x20 in frames_by_cmd:
    p = frames_by_cmd[0x20][-1]
    print(f"\n  0x20 (speed feedback?): {p[0]} (0x{p[0]:02X})")
    print(f"    This might be: 0=stopped, 1=moving")

if 0x22 in frames_by_cmd:
    p = frames_by_cmd[0x22][-1]
    print(f"\n  0x22 (cmd ack/error): {p[0]} (0x{p[0]:02X})")
    print(f"    0=success/accepted, nonzero=error code")
