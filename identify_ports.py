import serial
import time
import sys

ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
baudrates = [115200, 57600, 38400, 9600]

print("=== STARTING SERIAL PORT DISCOVERY ===")

for port in ports:
    print(f"\n----------------------------------------")
    print(f"Testing {port}...")
    
    found_data = False
    for baud in baudrates:
        try:
            ser = serial.Serial(port, baudrate=baud, timeout=0.5)
            # Read for 1.5 seconds
            start_time = time.time()
            buffer = bytearray()
            while time.time() - start_time < 1.5:
                data = ser.read(100)
                if data:
                    buffer.extend(data)
            ser.close()
            
            if len(buffer) > 0:
                found_data = True
                print(f"  [+] Baud {baud}: Read {len(buffer)} bytes")
                hex_sample = buffer[:32].hex()
                ascii_sample = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in buffer[:32]])
                print(f"      HEX:   {hex_sample}")
                print(f"      ASCII: {ascii_sample}")
                # Check header signatures
                if buffer[0] == 0x5a or buffer[0] == 0xa5:
                    print(f"      ==> MATCH: Keenon/Chassis Frame Header (0x5A / 0xA5)")
                if b'LIDAR' in buffer or b'SDK' in buffer or buffer[0] == 0xfa:
                    print(f"      ==> MATCH: Potential LiDAR Stream")
        except Exception as e:
            print(f"  [-] Error testing {port} at baud {baud}: {e}")
            
    if not found_data:
        print(f"  [-] No data received on {port} (port may be quiet until queried, or powered down)")

print("\n=== DISCOVERY COMPLETE ===")
