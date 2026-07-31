import serial
import time

bauds = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

print("=== SCANNING BAUD RATES ON /dev/ttyUSB1 ===")
for b in bauds:
    try:
        ser = serial.Serial('/dev/ttyUSB1', b, timeout=0.5)
        data = ser.read(50)
        ser.close()
        if data:
            print(f"  [SUCCESS] Baud {b}: Read {len(data)} bytes -> hex: {data.hex()} ascii: {data}")
        else:
            print(f"  [Empty] Baud {b}: No bytes received")
    except Exception as e:
        print(f"  [Error] Baud {b}: {e}")

print("Scan complete.")
