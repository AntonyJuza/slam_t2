import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== TESTING KEENON STM32 SPEED COMMAND (int16 vs int32) ===")

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

def send_cmd(cmd_id, payload):
    seq = 0x00
    length = len(payload)
    header = bytes([0xAA, 0xAA, 0x00, 0xE0, cmd_id, seq, length])
    checksum_val = sum(header[2:]) + sum(payload)
    crc = struct.pack('<H', checksum_val & 0xFFFF)
    packet = header + payload + crc + TAIL
    ser.write(packet)
    print(f"Sent CMD {hex(cmd_id)} (len {length}): {packet.hex()}")

# 1. Send Motor Enable / Unlock (CMD 0x21, payload 0x01)
send_cmd(0x21, bytes([0x01]))
time.sleep(0.1)

# 2. Send 4-byte payload (int16 linear_mm_s, int16 angular_mrad_s)
v_mm_s = 150 # 0.15 m/s forward
w_mrad_s = 0
payload_4byte = struct.pack('<hh', v_mm_s, w_mrad_s)
print("\nTesting 4-byte payload (int16, int16)...")
for _ in range(20):
    send_cmd(0x20, payload_4byte)
    time.sleep(0.05)

time.sleep(0.5)

# Stop motors
stop_payload = struct.pack('<hh', 0, 0)
send_cmd(0x20, stop_payload)

ser.close()
print("Test completed.")
