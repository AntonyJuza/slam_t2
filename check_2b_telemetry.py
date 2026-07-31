import serial
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
start = time.time()
buf = bytearray()

while time.time() - start < 1.0:
    if ser.in_waiting:
        buf.extend(ser.read(ser.in_waiting))
    time.sleep(0.05)

ser.close()

idx = 0
while idx < len(buf):
    if buf[idx:idx+2] == b'\xAA\xAA' and idx+10 <= len(buf):
        cmd = buf[idx+4]
        plen = buf[idx+6]
        payload = buf[idx+7:idx+7+plen]
        if cmd == 0x2B:
            print(f"Current 0x2B telemetry from STM32: {payload.hex()}")
            break
        idx += 7 + plen + 4
    else:
        idx += 1
