import serial
import time

for port in ['/dev/ttyUSB0', '/dev/ttyUSB1']:
    print(f"=== READING PORT {port} ===")
    try:
        ser = serial.Serial(port, 115200, timeout=1.0)
        data = ser.read(100)
        print(f"Data on {port} (115200 baud): {data}")
        ser.close()
    except Exception as e:
        print(f"Error on {port}: {e}")
