import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== TESTING KEENON MOTOR UNLOCK & MOTION COMMANDS ===")

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

def send_frame(cmd_id, payload):
    seq = 0x00
    length = len(payload)
    header = bytes([0xAA, 0xAA, 0x00, 0xE0, cmd_id, seq, length])
    checksum_val = sum(header[2:]) + sum(payload)
    crc = struct.pack('<H', checksum_val & 0xFFFF)
    packet = header + payload + crc + TAIL
    ser.write(packet)
    print(f"Sent CMD {hex(cmd_id)}: {packet.hex()}")

# 1. Send Motor Unlock command (CMD 0x21 with payload 0x01)
print("\nSending Motor Unlock (CMD 0x21, payload 0x01)...")
send_frame(0x21, bytes([0x01]))

time.sleep(0.2)

# 2. Also try CMD 0x2E with payload 0x01
send_frame(0x2E, bytes([0x01]))

time.sleep(0.2)

# 3. Read incoming status frames for 2 seconds
start_time = time.time()
buffer = bytearray()

while time.time() - start_time < 2.0:
    chunk = ser.read(256)
    if chunk:
        buffer.extend(chunk)

    while True:
        idx = buffer.find(HEADER)
        if idx == -1: break
        end_idx = buffer.find(TAIL, idx)
        if end_idx != -1:
            frame = buffer[idx:end_idx+2]
            buffer = buffer[end_idx+2:]
            if len(frame) >= 11:
                cmd_id = frame[4]
                length = frame[6]
                payload = frame[7:7+length]
                if cmd_id in [0x20, 0x21, 0x2C, 0x2E, 0x31, 0x41]:
                    print(f"  Received response CMD {hex(cmd_id)} (len {length}): {payload.hex()}")
        else:
            break

ser.close()
