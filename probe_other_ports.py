import serial
import time

ports = ['/dev/ttyUSB0', '/dev/ttyUSB1']

for p in ports:
    print(f"\n================ Probing {p} ================")
    try:
        ser = serial.Serial(p, 115200, timeout=1.0)
        data = ser.read(500)
        ser.close()
        print(f"Read {len(data)} bytes from {p}:")
        print(f"  HEX : {data.hex()[:100]}")
        print(f"  ASCII: {repr(data[:100])}")
    except Exception as e:
        print(f"Error opening {p}: {e}")
