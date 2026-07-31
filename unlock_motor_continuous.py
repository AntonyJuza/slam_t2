import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.05)
print("=== CONTINUOUS MOTOR UNLOCK & MOTION TEST ===")

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

def build_packet(cmd_id, payload):
    seq = 0x00
    length = len(payload)
    header = bytes([0xAA, 0xAA, 0x00, 0xE0, cmd_id, seq, length])
    checksum_val = sum(header[2:]) + sum(payload)
    crc = struct.pack('<H', checksum_val & 0xFFFF)
    return header + payload + crc + TAIL

start_time = time.time()
print("Sending unlock heartbeats + slow forward velocity (0.1 m/s)...")

try:
    while time.time() - start_time < 5.0:
        # 1. Send Motor Unlock command (0x2E with 0x01 and 0x21 with 0x01 and 0x28 with 0x01)
        p1 = build_packet(0x2E, bytes([0x01]))
        p2 = build_packet(0x21, bytes([0x01]))
        
        # 2. Send Velocity command (0.1 m/s = 100 mm/s forward)
        v_mm_s = 100
        w_mrad_s = 0
        speed_payload = struct.pack('<ii', v_mm_s, w_mrad_s)
        p3 = build_packet(0x20, speed_payload)

        ser.write(p1)
        ser.write(p2)
        ser.write(p3)

        time.sleep(0.05) # 20 Hz loop

        # Read responses
        chunk = ser.read(512)
        if chunk:
            idx = 0
            while True:
                idx = chunk.find(HEADER, idx)
                if idx == -1: break
                end_idx = chunk.find(TAIL, idx)
                if end_idx != -1:
                    frame = chunk[idx:end_idx+2]
                    if len(frame) >= 11:
                        cmd_id = frame[4]
                        length = frame[6]
                        payload = frame[7:7+length]
                        if cmd_id in [0x20, 0x21, 0x2E]:
                            print(f"Chassis status CMD {hex(cmd_id)}: payload={payload.hex()}")
                idx += 1

finally:
    # Stop motors
    stop_p = build_packet(0x20, struct.pack('<ii', 0, 0))
    ser.write(stop_p)
    ser.close()
    print("Done. Motors stopped.")
