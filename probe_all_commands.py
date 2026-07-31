import serial
import struct
import time

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.05)
print("=== PROBING STM32 CHASSIS COMMANDS & RESPONSES ===")

HEADER = bytes([0xAA, 0xAA])
TAIL = bytes([0x55, 0x55])

def send_frame(cmd_id, payload):
    seq = 0x00
    length = len(payload)
    header = bytes([0xAA, 0xAA, 0x00, 0xE0, cmd_id, seq, length])
    checksum_val = sum(header[2:]) + sum(payload)
    crc = struct.pack('<H', checksum_val & 0xFFFF)
    packet = header + payload + crc + TAIL
    ser.write(packet)
    return packet.hex()

def read_responses(duration=0.5):
    start = time.time()
    buf = bytearray()
    responses = []
    while time.time() - start < duration:
        chunk = ser.read(256)
        if chunk:
            buf.extend(chunk)
        while True:
            idx = buf.find(HEADER)
            if idx == -1: break
            end_idx = buf.find(TAIL, idx)
            if end_idx != -1:
                frame = buf[idx:end_idx+2]
                buf = buf[end_idx+2:]
                if len(frame) >= 11:
                    cmd = hex(frame[4])
                    length = frame[6]
                    p_hex = frame[7:7+length].hex()
                    responses.append((cmd, length, p_hex))
            else:
                break
    return responses

test_cmds = [
    (0x21, bytes([0x00])),
    (0x21, bytes([0x01])),
    (0x28, bytes([0x01])),
    (0x2E, bytes([0x00])),
    (0x2E, bytes([0x01])),
    (0x41, bytes([0x01])),
]

for cmd_id, payload in test_cmds:
    p_hex = send_frame(cmd_id, payload)
    print(f"\nSent {hex(cmd_id)} payload={payload.hex()} -> Packet: {p_hex}")
    resps = read_responses(0.3)
    for c, l, p in resps:
        print(f"   Received response CMD {c} (len {l}): {p}")

print("\nTesting speed command 0x20 (150 mm/s) after unlock...")
# Send unlock
send_frame(0x21, bytes([0x00]))
send_frame(0x2E, bytes([0x00]))

# Send speed
spd_payload = struct.pack('<hh', 150, 0)
for _ in range(10):
    send_frame(0x20, spd_payload)
    time.sleep(0.05)

resps = read_responses(0.5)
print("Responses during/after motion attempt:")
for c, l, p in resps:
    print(f"   Received CMD {c} (len {l}): {p}")

# Stop
send_frame(0x20, struct.pack('<hh', 0, 0))
ser.close()
print("Probing finished.")
