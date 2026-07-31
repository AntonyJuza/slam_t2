import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== REAL-TIME TELEMETRY MONITOR ===")
print("Monitoring 0x2B (battery), 0x2C (charging), 0x2E (motor lock), 0x41 (estop)...")
print("Press Ctrl+C to exit.\n")

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

# Continuously send unlock + speed, and print decoded status
start = time.time()
try:
    while True:
        # Send unlock + speed 100mm/s
        ser.write(build_pkt(0x21, b'\x01'))
        ser.write(build_pkt(0x20, struct.pack('<hh', 100, 0)))
        
        time.sleep(0.2)
        
        buf = ser.read(ser.in_waiting)
        # Parse status bytes from incoming frames
        status = {}
        idx = 0
        while idx < len(buf):
            if buf[idx:idx+2] == b'\xAA\xAA' and idx+10 <= len(buf):
                cmd = buf[idx+4]
                plen = buf[idx+6]
                payload = buf[idx+7:idx+7+plen]
                status[cmd] = payload
                idx += 7 + plen + 4
            else:
                idx += 1
                
        b_2b = status.get(0x2B, b'').hex()
        b_2c = status.get(0x2C, b'').hex()
        b_2e = status.get(0x2E, b'').hex()
        b_41 = status.get(0x41, b'').hex()
        b_2f = status.get(0x2F, b'').hex()
        
        t_rel = round(time.time() - start, 1)
        print(f"[{t_rel:5.1f}s] 0x2B(batt)={b_2b} | 0x2C(chg)={b_2c} | 0x2E(lock)={b_2e} | 0x41(estop)={b_41} | 0x2F(pwr)={b_2f[:8]}")
        time.sleep(0.3)
except KeyboardInterrupt:
    ser.write(build_pkt(0x20, struct.pack('<hh', 0, 0)))
    ser.close()
