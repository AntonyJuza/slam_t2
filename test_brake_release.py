import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)

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

print("=== TESTING ELECTROMAGNETIC BRAKE RELEASE PAYLOADS ===")
print("Sending various brake disengage/unlock commands to STM32...\n")

# Try CMD 0x21 with different payload values
unlock_test_values = [
    (0x21, b'\x00', "CMD 0x21 payload 0x00"),
    (0x21, b'\x01', "CMD 0x21 payload 0x01"),
    (0x21, b'\x02', "CMD 0x21 payload 0x02"),
    (0x21, b'\x04', "CMD 0x21 payload 0x04"),
    (0x21, b'\xFF', "CMD 0x21 payload 0xFF"),
    (0x28, b'\x00', "CMD 0x28 payload 0x00"),
    (0x28, b'\x01', "CMD 0x28 payload 0x01"),
    (0x29, b'\x01', "CMD 0x29 payload 0x01"),
]

for cmd, pay, desc in unlock_test_values:
    pkt = build_pkt(cmd, pay)
    print(f"Sending {desc}: {pkt.hex()}")
    ser.write(pkt)
    time.sleep(1.0)

ser.close()
print("\nFinished sending test unlock frames.")
