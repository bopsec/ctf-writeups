#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = [
#   "pycryptodome",
# ]
# ///
#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

key = os.urandom(16)
iv = os.urandom(16)

FLAG_val = os.getenv("FLAG")
if not FLAG_val:
    FLAG_val = hashlib.md5(os.urandom(16)).hexdigest()

FLAG = f"vil du ha dette?: {FLAG_val}"
FLAG = FLAG.encode()

def encrypt(pt):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(pt, 16))
    return ct.hex()

def decrypt(ct):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), 16)
    return pt

FLAGG = pad(FLAG, 16)
enc = encrypt(FLAG)
flag_blocks = []
for i in range(0, len(FLAGG), 16):
    flag_blocks.append(FLAG[i:i+16])

while True:
    try:
        line = input("> ")
        if not line:
            break
        option = int(line)
        if option == 1:
            pt = input("krypter melding > ")
            if not pt:
                break
            pt = pt.encode()
            ct = encrypt(pt)
            print(f"ct = {ct}")
        if option == 2:
            ct = input("skriv ciphertekst i hex> ")
            if not ct:
                break
            if len(ct) > 64:
                print("kan ikke håndtere")
                exit()
            try:
                pt = decrypt(bytes.fromhex(ct))
                if any(b in pt for b in flag_blocks):
                    print("juks")
                    exit()
                print(f"pt = {pt}")
            except:
                print("noe gikk galt")
    except (EOFError, KeyboardInterrupt):
        break
