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

print("=== TESTING DRIVE COMMAND WHILE BUTTON IS PRESSED VS RELEASED ===")
print("Sending continuous speed commands (300 mm/s forward)...")
print("Please PRESS the button (so motors are free), then RELEASE the button!\n")

start = time.time()
speed_payload = struct.pack('<hh', 300, 0)
unlock_payload = b'\x01'

try:
    while time.time() - start < 20.0:
        # Send unlock + speed continuously
        ser.write(build_pkt(0x21, unlock_payload))
        ser.write(build_pkt(0x20, speed_payload))
        
        # Read telemetry
        if ser.in_waiting:
            buf = ser.read(ser.in_waiting)
            # Check for CMD 0x41 or 0x2E or 0x2D
            idx = 0
            while idx < len(buf):
                if buf[idx:idx+2] == b'\xAA\xAA' and idx+11 <= len(buf):
                    cmd = buf[idx+4]
                    plen = buf[idx+6]
                    payload = buf[idx+7:idx+7+plen]
                    if cmd == 0x41:
                        print(f"[{time.time()-start:5.1f}s] Button (0x41): 0x{payload.hex()}")
                    elif cmd == 0x2E:
                        print(f"[{time.time()-start:5.1f}s] MotorLock (0x2E): 0x{payload.hex()}")
                    idx += 7 + plen + 4
                else:
                    idx += 1
        time.sleep(0.05)
finally:
    ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
    ser.close()
    print("Test finished. Brakes engaged.")
