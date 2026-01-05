#!/usr/bin/env python3
from pwn import *

conn = remote('apollo', 1337)

conn.recvuntil(b'Flagget er: ')
flag_ct = conn.recvline().decode().strip()
ct_blocks = [bytes.fromhex(flag_ct[i:i+32]) for i in range(0, len(flag_ct), 32)]
print(f"CT blocks: {len(ct_blocks)}")

def decrypt_hex(ct_hex):
    conn.recvuntil(b'> ')
    conn.sendline(b'2')
    conn.recvuntil(b'> ')
    conn.sendline(ct_hex.encode())
    return conn.recvline().decode().strip()

def attack_block(prev_block, target_block):
    """Padding oracle attack på én blokk"""
    intermediate = bytearray(16)

    for byte_pos in range(15, -1, -1):
        pad_val = 16 - byte_pos

        # Sett opp kjente bytes for riktig padding
        attack = bytearray(16)
        for i in range(byte_pos + 1, 16):
            attack[i] = intermediate[i] ^ pad_val

        for guess in range(256):
            attack[byte_pos] = guess
            ct = bytes(attack) + target_block
            result = decrypt_hex(ct.hex())

            if "noe gikk galt" not in result:
                intermediate[byte_pos] = guess ^ pad_val
                print(f"  Byte {byte_pos}: {chr(intermediate[byte_pos] ^ prev_block[byte_pos]) if 32 <= (intermediate[byte_pos] ^ prev_block[byte_pos]) < 127 else hex(intermediate[byte_pos] ^ prev_block[byte_pos])}")
                break

    # Plaintext = intermediate XOR prev_block
    return bytes(i ^ p for i, p in zip(intermediate, prev_block))

# Angrip blokk 3, 2, 1 (trenger forrige blokk som "IV")
print("\n=== Blokk 3 ===")
p3 = attack_block(ct_blocks[2], ct_blocks[3])
print(f"P3: {p3}")

print("\n=== Blokk 2 ===")
p2 = attack_block(ct_blocks[1], ct_blocks[2])
print(f"P2: {p2}")

print("\n=== Blokk 1 ===")
p1 = attack_block(ct_blocks[0], ct_blocks[1])
print(f"P1: {p1}")

print(f"\n=== FLAGG ===")
print(f"Blokk 1: {p1}")
print(f"Blokk 2: {p2}")
print(f"Blokk 3: {p3}")

conn.close()
