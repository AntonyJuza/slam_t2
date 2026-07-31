import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.05)
print("=== KEENON T2 BUTTON & MOTOR LOCK TELEMETRY MONITOR ===")
print("Please PRESS and RELEASE the red top button on the robot now!")
print("Observing CMD 0x41 (Button State) and CMD 0x2E (Motor Lock State)...\n")

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

start = time.time()
buf = bytearray()
last_41 = None
last_2e = None

try:
    while time.time() - start < 15.0:
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
                
                if cmd == 0x41 and len(payload) == 1:
                    val = payload[0]
                    if val != last_41:
                        print(f"[{time.time()-start:5.1f}s] >>> BUTTON STATE CHANGED (0x41): 0x{val:02X} ({'PRESSED/FREE' if val==0x01 else 'RELEASED/ENGAGED'})")
                        last_41 = val
                        
                elif cmd == 0x2E and len(payload) == 1:
                    val = payload[0]
                    if val != last_2e:
                        print(f"[{time.time()-start:5.1f}s] >>> MOTOR LOCK CHANGED (0x2E): 0x{val:02X}")
                        last_2e = val
        time.sleep(0.02)
finally:
    ser.close()
    print("\nMonitor completed.")
