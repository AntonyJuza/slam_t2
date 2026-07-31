import serial
import time

# Terminate ROS 2 driver temporarily if needed or read stream
ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== KEENON CHASSIS STATUS BYTE MONITOR ===")
print("Please press and release the E-stop button / manual brake lever...")

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

start = time.time()
buffer = bytearray()

while time.time() - start < 10.0:
    chunk = ser.read(256)
    if chunk:
        buffer.extend(chunk)

    while True:
        idx = buffer.find(HEADER)
        if idx == -1: break
        end_idx = buffer.find(TAIL, idx)
        if end_idx != -1:
            frame = buffer[idx:end_idx+2]
            buffer = buffer[end_idx+2:]
            if len(frame) >= 11:
                cmd = hex(frame[4])
                length = frame[6]
                payload = frame[7:7+length].hex()
                if frame[4] in [0x2A, 0x2B, 0x2C, 0x2E, 0x31, 0x41]:
                    print(f"Time {time.time()-start:5.2f}s | CMD {cmd}: payload={payload}")
        else:
            break

ser.close()
