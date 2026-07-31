import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.05)

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

def build_pkt(cmd_id, payload):
    hdr = bytes([0xE0, 0x00, cmd_id, 0x00, len(payload)])
    crc = struct.pack('<H', crc16_modbus(hdr + payload))
    return b'\xAA\xAA' + hdr + payload + crc + b'\x55\x55'

print("=== TESTING MOTION ENABLE MODES AND GOAL SIGNALS ===")

modes_to_test = [
    ("Mode CMD 0x40 val 0x01", 0x40, b'\x01'),
    ("Mode CMD 0x40 val 0x00", 0x40, b'\x00'),
    ("Mode CMD 0x28 val 0x01", 0x28, b'\x01'),
    ("Mode CMD 0x29 val 0x01", 0x29, b'\x01'),
    ("Mode CMD 0x21 val 0x00 (lock=False)", 0x21, b'\x00'),
    ("Mode CMD 0x21 val 0x01 (lock=True)", 0x21, b'\x01'),
]

speed_payload = struct.pack('<hh', 300, 0) # 300 mm/s

for desc, cmd_id, pay in modes_to_test:
    print(f"\n--- Testing {desc} ---")
    pkt = build_pkt(cmd_id, pay)
    print(f"Sending setup pkt: {pkt.hex()}")
    ser.write(pkt)
    time.sleep(0.1)
    
    # Now send 30 speed packets
    for _ in range(30):
        ser.write(build_pkt(0x20, speed_payload))
        time.sleep(0.03)
    
    time.sleep(0.2)
    ser.reset_input_buffer()

# Stop
ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()
print("Motion mode test complete.")
