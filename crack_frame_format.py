#!/usr/bin/env python3
"""
Reverse engineer the EXACT CRC used by Keenon STM32.
We have known frames from the STM32 - let's find what CRC matches.
"""
import struct

# Known frames from STM32 (with their CRC bytes)
# Frame: AA AA [src] [dst] [cmd] [seq] [len] [payload...] [crc_lo] [crc_hi] 55 55
#
# CMD 0x20: aaaa 00 e0 20 00 01 00  39 1d  75 5555
#   BUT WAIT - let me reparse this more carefully
#   aaaa = header
#   00 = byte2
#   e0 = byte3  
#   20 = byte4 (cmd)
#   00 = byte5 (seq)
#   01 = byte6 (len=1)
#   00 = byte7 (payload, 1 byte)
#   39 1d = CRC (2 bytes)
#   75 5555 = WAIT, that's 3 bytes not 2!
#
# Hmm, let me re-examine. The raw hex: aaaa00e020000100391d755555
# Let me count bytes:
# aa aa  00 e0  20 00  01 00  39 1d  75 55 55
# 2      2      2      2      2      3  ← doesn't work for 0x55 0x55 tail
#
# Alternative parsing:
# aa aa 00 e0 20 00 01 00 39 1d 75 55 55
# hdr   s  d  c  sq ln p  ?  ?  ?  tail
#
# Wait, len=1 means payload is 1 byte. So:
# aa aa [00] [e0] [20] [00] [01] [00] [CRC1] [CRC2] [55] [55]
#                                      ^^payload     ^^^^CRC   ^^^^tail
# That gives: payload = 0x00, CRC = 0x39 0x1D, then 0x75 0x55 0x55
# But that's 3 bytes after CRC, not 2 for tail!
#
# UNLESS the tail is not 0x5555 but something else, or
# the CRC is 3 bytes, or the frame has extra bytes

# Let me re-examine frame structure more carefully
raw_frames = [
    bytes.fromhex("aaaa00e020000100391d755555"),  # CMD 0x20
    bytes.fromhex("aaaa00e2220001003164915555"),  # CMD 0x22
]

for raw in raw_frames:
    print(f"\nFrame: {raw.hex()}")
    print(f"  Length: {len(raw)} bytes")
    print(f"  Bytes: {' '.join(f'{b:02X}' for b in raw)}")
    
    # Try different structure interpretations
    # Interpretation 1: header(2) + src(1) + dst(1) + cmd(1) + seq(1) + len(1) + payload(len) + crc(2) + tail(2)
    # For len=1: total = 2+1+1+1+1+1+1+2+2 = 12 bytes. But frame is 13 bytes!
    
    # Interpretation 2: Maybe there's an extra byte somewhere
    # header(2) + type(1) + src(1) + dst(1) + cmd(1) + seq(1) + len(1) + payload(len) + crc(2) + tail(2)
    # For len=1: total = 2+1+1+1+1+1+1+1+2+2 = 13 bytes. ← MATCHES!
    
    print("\n  Interpretation: header(2) + type(1) + addr(1) + cmd(1) + seq(1) + len(1) + payload + crc(2) + tail(2)")
    if len(raw) >= 13:
        hdr = raw[0:2]
        frame_type = raw[2]
        addr = raw[3]
        cmd = raw[4]
        seq = raw[5]
        plen = raw[6]
        payload = raw[7:7+plen]
        crc_bytes = raw[7+plen:9+plen]
        tail = raw[9+plen:]
        
        print(f"    Header: {hdr.hex()}")
        print(f"    Type/Src: 0x{frame_type:02X}")
        print(f"    Addr/Dst: 0x{addr:02X}")
        print(f"    CMD: 0x{cmd:02X}")
        print(f"    SEQ: 0x{seq:02X}")
        print(f"    LEN: {plen}")
        print(f"    Payload: {payload.hex()}")
        print(f"    CRC: {crc_bytes.hex()} (LE=0x{struct.unpack('<H', crc_bytes)[0]:04X})")
        print(f"    Tail: {tail.hex()}")

# Wait, the CMD 0x20 frame:
# AA AA 00 E0 20 00 01 00 39 1D 75 55 55
# If len=1, payload=0x00, crc=0x391D, tail=0x755555 ← 3-byte tail doesn't make sense
#
# BUT if I look again at all our earlier probe results, the frames with len=1 had:
# CMD 0x2E: "Time 2.21s | CMD 0x2e: payload=00"
# That was parsed correctly with our simple parser which found 0x5555 tail
#
# So maybe CMD 0x20's raw hex is being shown incorrectly, or the frame has different structure

# Let me try: maybe len=01 but the payload is actually "00 39 1D 75" (4 bytes) and 
# the len field means something different for CMD 0x20 responses?

# OR: maybe the frame is:
# AA AA 00 E0 20 00 01  00 39  1D75 5555
# hdr(2) ?? ?? cmd sq len  pay(1) crc(2) tail(2)  <- but that gives crc=0x0039, tail=1D755555?

# Let me just brute-force: for each possible CRC position, check all CRC algorithms
print("\n\n=== BRUTE FORCE CRC SEARCH ===")

frame1 = bytes.fromhex("aaaa00e020000100391d755555")

# The frame MUST end with 55 55. So if tail = 55 55:
# Frame without tail: aaaa00e02000010039 1D75
# That's 11 bytes before tail = header(2) + 5 control + payload + CRC
# If len=1 and payload=1 byte: 2+5+1=8 data bytes + CRC
# CRC could be at position 8: bytes[8:10] = 0x39 0x1D, but then 0x75 is extra
# CRC could be at position 8: bytes[8:11] = 0x39 0x1D 0x75 (3 byte CRC?)

# What if the tail is just 0x55 (1 byte)?
# Frame without 1-byte tail: aaaa00e020000100391d75 55
# = 12 bytes + tail. Header(2) + 5 + 1 payload = 8, CRC = bytes[8:12] = 39 1D 75 55? 4-byte CRC?

# What if byte 6 is NOT the length?
# Let's try: what if the header is: AA AA [00] [E0] [CMD] [LEN_HI] [LEN_LO]
# Then len = 0x0001 = 1 byte payload, same result

# What if len includes CRC? len=1 means 1 byte after the header including everything?
# Doesn't make sense with frame sizes

# Let me look at a frame I KNOW the structure of from our earlier CRC discovery:
# From find_crc16.py, we verified CRC16-Modbus on data "00E02D000C" + encoder_payload
# That frame would be: AA AA 00 E0 2D 00 0C [12 bytes payload] [2 bytes CRC] 55 55
# Total = 2 + 5 + 12 + 2 + 2 = 23 bytes

# So for the CMD 0x20 frame: AA AA 00 E0 20 00 01 [1 byte payload] [2 bytes CRC] 55 55
# Total should be = 2 + 5 + 1 + 2 + 2 = 12 bytes
# But the actual frame is 13 bytes! There's an extra byte.

# Let me check: maybe I grabbed the wrong tail position
# aaaa00e020000100391d755555
# Positions: 0123456789...
# 0-1: AA AA (header)
# 2: 00
# 3: E0
# 4: 20 (cmd)
# 5: 00 (seq)
# 6: 01 (len)
# 7: 00 (payload byte 0)
# 8-9: 39 1D (CRC)
# 10-11: 75 55 ← NOT 55 55!
# 12: extra 55

# AH HA! Positions 10-11 are 0x75 0x55, and position 12 is 0x55
# So the tail is at positions 11-12: 0x55 0x55
# That means the CRC is at positions 8-10: 0x39 0x1D 0x75 (3 bytes?!)
# OR there's extra data between CRC and tail

# Wait - let me reconsider. What if HEADER is different for this frame type?
# What if it's AA AA 00 E0 20 00 01 00  = 8 bytes of header/meta
# Then comes CRC starting at position 8: 39 1D = 2 bytes
# Then 75 55 55 = can't be tail

# Unless the frame is: 
# AA AA 00 E0 20 00  01 00 39  1D 75  55 55
#                    ^^^^^^^^^^  ^^^^  ^^^^
#                    payload(3)  CRC   tail
# But then len=0x00 and byte6=0x20? That makes no sense

# NEW IDEA: What if the frame structure in the STM32->PC direction is:
# AA AA [device_type] [??] [cmd] [seq] [len_lo] [len_hi] [payload] [crc] [55 55]
# With len as uint16: 0x0001
# Then: payload = 0x00, one byte after that = crc_lo = 0x39, crc_hi = 0x1D
# Still 0x75 extra

# SIMPLEST explanation: The frame parsing picked up a stray 0xAA 0xAA before
# the actual frame start, or there's a nested frame.

# Let me search for 5555 in the frame and work backwards
print("\nSearching for valid frame boundaries in raw data...")
raw = bytes.fromhex("aaaa00e020000100391d755555")
for i in range(len(raw)-1):
    if raw[i] == 0x55 and raw[i+1] == 0x55:
        print(f"  Found 5555 at position {i}")
        # Everything before this is header+data+crc
        before_tail = raw[:i]
        print(f"  Before tail: {before_tail.hex()} ({len(before_tail)} bytes)")
        # If CRC is 2 bytes:
        if len(before_tail) >= 4:
            crc_2 = before_tail[-2:]
            data = before_tail[2:-2]  # skip AA AA
            print(f"  Data for CRC: {data.hex()}")
            print(f"  CRC in frame: {crc_2.hex()} = 0x{struct.unpack('<H', crc_2)[0]:04X}")
            
            # Test additive
            add_sum = sum(data) & 0xFFFF
            print(f"  Additive sum: 0x{add_sum:04X}")
            
            # Test modbus
            def crc16_modbus(d):
                c = 0xFFFF
                for b in d:
                    c ^= b
                    for _ in range(8):
                        if c & 1: c = (c >> 1) ^ 0xA001
                        else: c >>= 1
                return c & 0xFFFF
            
            mod_crc = crc16_modbus(data)
            print(f"  Modbus CRC:   0x{mod_crc:04X}")
