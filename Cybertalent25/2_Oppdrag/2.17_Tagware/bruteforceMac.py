enc_cmd = bytes.fromhex(
    "2f07c4441521d8ad72579b12067bdfa87e059d120776d8fd"
    "72079e4a0127deaa2b06c8490c62d5f76a1a8305463183e6"
    "2b11d8435a3082b32f00f340503b98"
)

low = [0x4a,0x64,0xac,0x2b,0x35,0x42]

def is_printable(bs):
    return all(32 <= b < 127 or b in (9,10,13,0) for b in bs)

def contains_crib(bs):
    return b".ssh/authorized_keys" in bs

for k6 in range(256):
    for k7 in range(256):
        key = low + [k6,k7]
        dec = bytes(enc_cmd[i] ^ key[i & 7] for i in range(len(enc_cmd)))
        if is_printable(dec) and contains_crib(dec):
            print("KEY:", bytes(key).hex())
            print(dec)
