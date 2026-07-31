import serial
import struct
import time
import math

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
print("=== KEENON T2 REAL-TIME TELEMETRY DECODER ===")

prev_left = None
prev_right = None
prev_time = time.time()

buffer = bytearray()
start_time = time.time()
frame_count = 0

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

try:
    while time.time() - start_time < 5.0:
        chunk = ser.read(256)
        if chunk:
            buffer.extend(chunk)

        while True:
            # Locate next header AA AA
            idx = buffer.find(HEADER)
            if idx == -1:
                # Keep last byte in case header is split across reads
                if len(buffer) > 1:
                    buffer = buffer[-1:]
                break

            if idx > 0:
                buffer = buffer[idx:] # Trim pre-header noise

            if len(buffer) < 11:
                break # Need header + cmd + len

            cmd_id = buffer[4]
            seq_id = buffer[5]
            payload_len = buffer[6]

            frame_len = 7 + payload_len + 2 + 2 # 7 header + payload + 2 CRC + 2 Tail
            if len(buffer) < frame_len:
                break # Wait for complete frame

            frame = buffer[:frame_len]
            buffer = buffer[frame_len:]

            if frame[-2:] == TAIL:
                frame_count += 1
                payload = frame[7:7+payload_len]

                if cmd_id == 0x2D and payload_len == 12:
                    cur_vel_raw, left_ticks, right_ticks = struct.unpack('<iii', payload)
                    now = time.time()
                    dt = now - prev_time

                    if prev_left is not None:
                        dl = left_ticks - prev_left
                        dr = right_ticks - prev_right
                        print(f"[{frame_count:04d}] CMD 0x2D (ODOM) | Left: {left_ticks:10d} (Δ{dl:+4d}) | Right: {right_ticks:10d} (Δ{dr:+4d}) | VelRaw: {cur_vel_raw}")

                    prev_left = left_ticks
                    prev_right = right_ticks
                    prev_time = now

                elif cmd_id == 0x32 and payload_len == 16:
                    # IMU Acc / Gyro
                    ax, ay, az, gz = struct.unpack('<ffff', payload)
                    print(f"[{frame_count:04d}] CMD 0x32 (IMU)  | Acc: ({ax:+.2f}, {ay:+.2f}, {az:+.2f}) | GyroZ: {gz:+.3f}")

except Exception as e:
    print(f"Error: {e}")

ser.close()
print(f"\nDone. Successfully parsed {frame_count} frames from STM32 chassis.")
