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

print("=== INJECTING BATTERY = 100% (0x2B) TO STM32 ===")

# Try sending battery 100% frames to STM32
battery_payloads = [
    b'\x64\x00', # 100%, state 0
    b'\x64\x96', # 100%, state 0x96
    b'\x64\x01', # 100%, state 1
    b'\xFF\xFF', # Max
]

for pay in battery_payloads:
    print(f"\nInjecting 0x2B payload: {pay.hex()}")
    for _ in range(10):
        ser.write(build_pkt(0x2B, pay))
        ser.write(build_pkt(0x21, b'\x01')) # unlock
        ser.write(build_pkt(0x20, struct.pack('<hh', 300, 0))) # speed 300mm/s
        time.sleep(0.05)
    
    time.sleep(0.2)

ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
ser.close()
print("Battery injection test finished.")
