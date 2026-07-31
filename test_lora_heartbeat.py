import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
print("=== TESTING LORA / INTERLOCK HEARTBEAT ON /dev/ttyUSB0 ===")

start = time.time()
try:
    while time.time() - start < 5.0:
        if ser.in_waiting > 0:
            msg = ser.read(ser.in_waiting)
            print(f"Received from USB0 ({len(msg)} bytes): {msg}")
            # Echo back or send heartbeat response
            ser.write(b"~^0`\n")
            ser.write(b"OK\r\n")
        time.sleep(0.1)
finally:
    ser.close()
    print("Test finished.")
