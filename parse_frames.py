import serial
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=1.0)
print("Listening to /dev/ttyUSB2...")

buffer = bytearray()
frames = []

start = time.time()
while time.time() - start < 3.0:
    chunk = ser.read(256)
    if chunk:
        buffer.extend(chunk)

ser.close()

print(f"Total raw bytes collected: {len(buffer)}")

# Search for header patterns: 0x55 0xaa or 0xaa 0xaa
idx = 0
while idx < len(buffer) - 10:
    # Look for 0x55 0xaa 0xaa or 0xaa 0xaa
    if buffer[idx] == 0xaa and buffer[idx+1] == 0xaa:
        frame_start = idx
        # Find next header or extract fixed length
        next_idx = idx + 2
        while next_idx < len(buffer) - 1:
            if buffer[next_idx] == 0xaa and buffer[next_idx+1] == 0xaa:
                break
            next_idx += 1
        
        frame = buffer[frame_start:next_idx]
        if len(frame) >= 6:
            frames.append(frame)
        idx = next_idx
    else:
        idx += 1

print(f"\nFound {len(frames)} frames starting with 0xAA 0xAA:")
for i, f in enumerate(frames[:15]):
    print(f"Frame {i+1} (len {len(f)}): {f.hex()}")
