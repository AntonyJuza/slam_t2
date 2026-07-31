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

print("=== TESTING VARIOUS SPEED SCALES FOR CMD 0x20 ===")

# Send unlock
ser.write(build_pkt(0x21, b'\x01'))
time.sleep(0.1)

speed_tests = [
    ("v=100 (100 mm/s = 0.1 m/s)", struct.pack('<hh', 100, 0)),
    ("v=300 (300 mm/s = 0.3 m/s)", struct.pack('<hh', 300, 0)),
    ("v=500 (500 mm/s = 0.5 m/s)", struct.pack('<hh', 500, 0)),
    ("v=1000 (1000 mm/s = 1.0 m/s)", struct.pack('<hh', 1000, 0)),
    ("v=30 (30 cm/s = 0.3 m/s)", struct.pack('<hh', 30, 0)),
    ("v=3000 (3000 unit)", struct.pack('<hh', 3000, 0)),
    ("v=10000 (10000 unit)", struct.pack('<hh', 10000, 0)),
]

for desc, payload in speed_tests:
    print(f"\nTesting {desc} - sending 20 frames...")
    ser.reset_input_buffer()
    for _ in range(20):
        ser.write(build_pkt(0x20, payload))
        time.sleep(0.05)
    
    # Read response
    time.sleep(0.2)
    buf = ser.read(ser.in_waiting)
    print(f"Read {len(buf)} response bytes.")

# Stop
ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()
print("Speed scale test complete.")
