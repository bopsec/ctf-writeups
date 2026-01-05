enc_sym = bytes([0x20,0x0f,0xc8,0x4e,0x42,0x21])
target  = b"jkdewc"

# utled laveste 6 bytes av uVar1
low = [enc_sym[i] ^ target[i] for i in range(6)]

# de to øverste byte er ukjent → brute force 16 bit
for hi in range(0x10000):
    key = bytearray(low + [hi & 0xff, hi >> 8])
    uVar1 = int.from_bytes(key, "little")

    # verifiser mot hele dekrypteringen i main
    ok = True
    for i in range(6):
        if (uVar1 >> ((i*8)&0x3f) & 0xff) ^ enc_sym[i] != target[i]:
            ok = False
            break
    if ok:
        print("FOUND uVar1 =", hex(uVar1))
        break
