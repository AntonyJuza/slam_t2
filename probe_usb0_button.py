import serial
import time

print("=== PROBING LORA / SAFETY BOARD ON /dev/ttyUSB0 ===")
print("Please PRESS and RELEASE the red top button now!")
print("Reading serial streams from /dev/ttyUSB0 for 15 seconds...\n")

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
start = time.time()
last_line = ""

try:
    while time.time() - start < 15.0:
        line = ser.readline()
        if line:
            line_str = line.decode('ascii', errors='ignore').strip()
            if line_str != last_line:
                print(f"[{time.time()-start:5.1f}s] USB0 Output Changed: '{line_str}' (raw: {line})")
                last_line = line_str
        time.sleep(0.02)
finally:
    ser.close()
    print("\nProbe complete.")
