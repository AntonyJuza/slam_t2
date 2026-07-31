import struct

# Sample Keenon Frame 2:
# Header: AA AA 00 E0 2D 00 0C
# Payload: 00 00 00 00 00 1D 4E 19 00 22 4E 19 00
# Target CRC bytes in frame: E4 34 -> int16 0x34E4 (13540) or 0xE434

frame_data = bytes.fromhex("00E02D000C" + "00000000001D4E1900224E1900")
target_crc_le = 0x34E4
target_crc_be = 0xE434

print(f"Target CRC bytes: 0xE434 or 0x34E4")
print(f"Testing CRC algorithms on frame data: {frame_data.hex()}")

# 1. CRC16-MODBUS (poly 0x8005 / 0xA001, init 0xFFFF)
def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

# 2. CRC16-CCITT / FALSE (poly 0x1021, init 0xFFFF)
def crc16_ccitt_false(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

# 3. CRC16-XMODEM (poly 0x1021, init 0x0000)
def crc16_xmodem(data: bytes) -> int:
    crc = 0x0000
    for b in data:
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

# 4. CRC16-X25 (poly 0x1021, init 0xFFFF, xorout 0xFFFF, ref-in/out)
def crc16_x25(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        # reflect byte
        b = int(f'{b:08b}'[::-1], 2)
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    # reflect crc
    crc = int(f'{crc:016b}'[::-1], 2)
    return (crc ^ 0xFFFF) & 0xFFFF

# Test all combinations of init (0x0000, 0xFFFF), poly (0x1021, 0x8005, 0xA001, 0x8408), ref-in/out, xorout
print(f"CRC16 Modbus: {hex(crc16_modbus(frame_data))}")
print(f"CRC16 CCITT:  {hex(crc16_ccitt_false(frame_data))}")
print(f"CRC16 XModem: {hex(crc16_xmodem(frame_data))}")
print(f"CRC16 X25:    {hex(crc16_x25(frame_data))}")

# Full brute-force scan over polynomials and initial values
found = False
for poly in [0x1021, 0x8005, 0x8408, 0xA001, 0x3D65]:
    for init in [0x0000, 0xFFFF, 0x1D0F]:
        for xorout in [0x0000, 0xFFFF]:
            # Non-reflected
            crc = init
            for b in frame_data:
                crc ^= (b << 8)
                for _ in range(8):
                    if crc & 0x8000:
                        crc = ((crc << 1) ^ poly) & 0xFFFF
                    else:
                        crc = (crc << 1) & 0xFFFF
            res = (crc ^ xorout) & 0xFFFF
            if res in (target_crc_le, target_crc_be):
                print(f"MATCH FOUND! Non-reflected: Poly={hex(poly)}, Init={hex(init)}, XorOut={hex(xorout)} -> {hex(res)}")
                found = True

            # Reflected
            crc = init
            for b in frame_data:
                b_ref = int(f'{b:08b}'[::-1], 2)
                crc ^= b_ref
                for _ in range(8):
                    if crc & 0x0001:
                        crc = (crc >> 1) ^ poly
                    else:
                        crc >>= 1
            res = (crc ^ xorout) & 0xFFFF
            if res in (target_crc_le, target_crc_be):
                print(f"MATCH FOUND! Reflected: Poly={hex(poly)}, Init={hex(init)}, XorOut={hex(xorout)} -> {hex(res)}")
                found = True

if not found:
    print("No simple CRC match on full payload; checking including full header AA AA...")
    full_data = bytes.fromhex("AAAA00E02D000C00000000001D4E1900224E1900")
    for poly in [0x1021, 0x8005, 0x8408, 0xA001]:
        for init in [0x0000, 0xFFFF]:
            for xorout in [0x0000, 0xFFFF]:
                crc = init
                for b in full_data:
                    b_ref = int(f'{b:08b}'[::-1], 2)
                    crc ^= b_ref
                    for _ in range(8):
                        if crc & 0x0001:
                            crc = (crc >> 1) ^ poly
                        else:
                            crc >>= 1
                res = (crc ^ xorout) & 0xFFFF
                if res in (target_crc_le, target_crc_be):
                    print(f"MATCH FOUND on FULL DATA! Poly={hex(poly)}, Init={hex(init)}, XorOut={hex(xorout)} -> {hex(res)}")
