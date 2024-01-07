def sub_140074060(a1):
    # Perform the operation, ensuring each step stays within 32-bit range
    result = (32 * (((((a1 << 13) & 0xFFFFFFFF) ^ a1) >> 17) ^ ((a1 << 13) & 0xFFFFFFFF) ^ a1)) ^ (((((a1 << 13) & 0xFFFFFFFF) ^ a1) >> 17) ^ ((a1 << 13) & 0xFFFFFFFF) ^ a1)
    # Ensure result is within 32-bit range
    return result & 0xFFFFFFFF

dword_1401A9930 = [ 0x48, 0x9D, 0x23B, 0x28, 0x5A, 0x7, 0xF5, 0x121, 0x57, 0x10C,
                    0x288, 0xF1, 0x1F, 0x36, 0x251, 0x40, 0x4F, 0xAA, 0x143, 0xED,
                    0x183, 0x5, 0xCB, 0x306, 0x88, 0x26C, 0x8E, 0x10E, 0x33, 0x111,
                    0x15E, 0x2C5, 0x79, 0x84, 0x24B, 0x6F, 0x1B, 0x0]

captions = ""

def start_address(lpThreadParameter):
    global captions
    v2 = 1337 * (lpThreadParameter + 1)
    v25 = dword_1401A9930[lpThreadParameter]

    for i in range(v25):
        v2 = sub_140074060(v2)
    message = "Hemmelighet"
    caption = chr(v2 & 0xFF)
    captions = captions + caption
    print(f"MessageBox: {message}, Caption: {caption}")

for i in range(37):
    start_address(i)

print(captions)
