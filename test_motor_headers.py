import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.05)
print("=== TESTING SENDER/RECEIVER HEADER TARGET IDs FOR MOTOR COMMAND ===")

HEADER_1 = bytes([0xAA, 0xAA, 0x00, 0xE0]) # Chassis 0x00 -> PC 0xE0
HEADER_2 = bytes([0xAA, 0xAA, 0xE0, 0x00]) # PC 0xE0 -> Chassis 0x00
TAIL = bytes([0x55, 0x55])

def send_pkt(hdr_prefix, cmd_id, payload):
    seq = 0x00
    length = len(payload)
    hdr = hdr_prefix + bytes([cmd_id, seq, length])
    checksum_val = sum(hdr[2:]) + sum(payload)
    crc = struct.pack('<H', checksum_val & 0xFFFF)
    pkt = hdr + payload + crc + TAIL
    ser.write(pkt)
    print(f"Sent {pkt.hex()}")

# 1. Test HEADER_2 (E0 00) with 200 mm/s speed
v_mm_s = 200
w_mrad_s = 0
payload = struct.pack('<hh', v_mm_s, w_mrad_s)

print("\n--- Testing HEADER (AA AA E0 00) ---")
for _ in range(20):
    send_pkt(HEADER_2, 0x20, payload)
    time.sleep(0.05)

time.sleep(0.5)

# Stop
stop_payload = struct.pack('<hh', 0, 0)
send_pkt(HEADER_2, 0x20, stop_payload)

ser.close()
print("Test completed.")
