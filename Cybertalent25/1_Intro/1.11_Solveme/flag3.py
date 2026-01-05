hardcoded = [0x8f745590, 0x6b838889, 0x8c5d8485, 0x6283616a]
counters = [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f]

password = b""
for i in range(4):
    val = (hardcoded[i] - 0x23232323) & 0xFFFFFFFF
    val ^= counters[i]
    password += val.to_bytes(4, 'little')

print(password)