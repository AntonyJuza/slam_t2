import serial
import struct
import time
import math

# Kinematic parameters from T2 chassis_params.yaml
WHEEL_GAUGE = 0.366       # 366.0 mm track width (m)
WHEEL_PERIMETER = 0.5172  # 517.2 mm circumference (m)
TICKS_PER_REV = 4096.0    # Typical 12-bit magnetic encoder resolution or scale factor

print("=== KEENON T2 CHASSIS REAL-TIME TELEMETRY DECODER ===")
print("Opening /dev/ttyUSB2 at 115200 baud...\n")

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)

prev_left_ticks = None
prev_right_ticks = None
prev_time = time.time()

x_pos = 0.0
y_pos = 0.0
theta = 0.0

buffer = bytearray()

try:
    while True:
        data = ser.read(128)
        if data:
            buffer.extend(data)

        # Process frames in buffer
        while len(buffer) >= 10:
            # Search for 0xAA 0xAA header
            if buffer[0] != 0xAA or buffer[1] != 0xAA:
                buffer.pop(0)
                continue

            # Need at least header + target + cmd + len (7 bytes)
            if len(buffer) < 7:
                break

            target = buffer[2:4]
            cmd_id = buffer[4]
            # payload length (little or big endian - in sample 0x000C = 12)
            payload_len = (buffer[5] << 8) | buffer[6]
            
            # Full frame size = 2 (header) + 2 (target) + 1 (cmd) + 2 (len) + payload_len + 2 (crc) + 2 (tail 55 55)
            total_frame_len = 2 + 2 + 1 + 2 + payload_len + 2 + 2
            
            if len(buffer) < total_frame_len:
                break # Wait for complete frame

            frame = buffer[:total_frame_len]
            buffer = buffer[total_frame_len:] # Consume frame

            # Verify frame tail 0x55 0x55
            if frame[-2] != 0x55 or frame[-1] != 0x55:
                continue

            payload = frame[7:7+payload_len]

            # CMD 0x2D: Encoder and Linear Velocity Telemetry
            if cmd_id == 0x2D and payload_len == 12:
                cur_vel_raw, left_ticks, right_ticks = struct.unpack('<iii', payload)
                now = time.time()
                dt = now - prev_time

                if prev_left_ticks is not None and dt > 0:
                    d_left_ticks = left_ticks - prev_left_ticks
                    d_right_ticks = right_ticks - prev_right_ticks

                    # Calculate distance traveled by each wheel (m)
                    # Note: We scale using TICKS_PER_REV or encoder delta
                    d_left_m = (d_left_ticks / TICKS_PER_REV) * WHEEL_PERIMETER
                    d_right_m = (d_right_ticks / TICKS_PER_REV) * WHEEL_PERIMETER

                    d_center = (d_left_m + d_right_m) / 2.0
                    d_theta = (d_right_m - d_left_m) / WHEEL_GAUGE

                    x_pos += d_center * math.cos(theta + d_theta/2.0)
                    y_pos += d_center * math.sin(theta + d_theta/2.0)
                    theta += d_theta

                    v_lin = d_center / dt
                    v_ang = d_theta / dt

                    print(f"[ODOM 0x2D] L_Ticks: {left_ticks:10d} (Δ{d_left_ticks:+4d}) | R_Ticks: {right_ticks:10d} (Δ{d_right_ticks:+4d}) | V_lin: {v_lin:+6.3f} m/s | V_ang: {v_ang:+6.3f} rad/s | Pose: X={x_pos:6.3f}m, Y={y_pos:6.3f}m, θ={math.degrees(theta):+6.1f}°")

                prev_left_ticks = left_ticks
                prev_right_ticks = right_ticks
                prev_time = now

except KeyboardInterrupt:
    print("\nStopped.")
    ser.close()
