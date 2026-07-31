import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== TESTING KEENON CHASSIS MOTION WITH VALID CRC16-MODBUS ===")

HEADER = bytes([0xAA, 0xAA, 0xE0, 0x00]) # PC 0xE0 -> Chassis 0x00
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

def build_valid_packet(cmd_id, payload):
    seq = 0x00
    length = len(payload)
    hdr_bytes = bytes([0xE0, 0x00, cmd_id, seq, length]) # Data over which CRC is calculated
    data_to_crc = hdr_bytes + payload
    
    crc_val = crc16_modbus(data_to_crc)
    crc_bytes = struct.pack('<H', crc_val) # Little-endian CRC16
    
    packet = bytes([0xAA, 0xAA]) + hdr_bytes + payload + crc_bytes + TAIL
    return packet

# 1. Send Motor Unlock (CMD 0x21, payload 0x01)
p_unlock = build_valid_packet(0x21, bytes([0x01]))
print(f"Sending Unlock Packet with valid CRC16: {p_unlock.hex()}")
ser.write(p_unlock)
time.sleep(0.1)

# 2. Send Forward Velocity (200 mm/s = 0.2 m/s) for 2 seconds
v_mm_s = 200
w_mrad_s = 0
speed_payload = struct.pack('<hh', v_mm_s, w_mrad_s)
p_speed = build_valid_packet(0x20, speed_payload)

print(f"Sending Speed Packet (0.2 m/s forward) with valid CRC16: {p_speed.hex()}")
print("Motors should turn NOW! Sending 40 speed frames...")

start = time.time()
for _ in range(40):
    ser.write(p_speed)
    time.sleep(0.05)

# 3. Stop
p_stop = build_valid_packet(0x20, struct.pack('<hh', 0, 0))
ser.write(p_stop)
ser.close()
print("Motion test finished. Brakes engaged.")
