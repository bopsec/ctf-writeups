import hashlib
import struct

# secp256k1 curve order
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

encrypted = bytes.fromhex('7766cf33529a22e3adc0b028fa9da62ee10f47c39e16ab1035f95d5bf2cf3ca3')

# Signature values extracted from the two inputs (same r, nonce reuse)
r = 0x585ab36f9f554049f045bd9c9347a4045aa7ad5f666dc4e72c19c4ba7921ac36
s1 = 0xa663a41bd336c5730010ea8ad1a6284dcfcd77237797d740774b7e7146aa723d
s2 = 0x916b7958e8ea912b960766502afaa16b28ade3e30239bbef430acec974ba46c1

# Previous outputs being spent
prev_txid1 = bytes.fromhex("91c406e3947eb80e27f976424c2b927f13e6f258be32d8267cf82474a1775027")[::-1]
prev_txid2 = bytes.fromhex("70ac03d052cab253aeb40aeb499c20512ef7597f8d7f7cf4c5451c801d358072")[::-1]

# scriptPubKey (P2PKH for address 17jtMiimZG2F8FhZm46Rr77Ue4BjmHZB5x)
scriptPubKey = bytes.fromhex("76a91449ed1890721804d1fa6164a4ccc512aabc68d7d088ac")

# Output value and script
out_value = struct.pack('<Q', 200000)
out_script = bytes.fromhex("76a91449ed1890721804d1fa6164a4ccc512aabc68d7d088ac")


def inverse_mod(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1
    if a < 0:
        a = a % m
    g, x, _ = extended_gcd(a, m)
    return x % m

def dsha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def build_sighash(input_index):
    tx = b''
    tx += struct.pack('<I', 1)  # version
    tx += b'\x02'  # input count
    
    # Input 0
    tx += prev_txid1 + struct.pack('<I', 1)  # txid + vout
    tx += (bytes([len(scriptPubKey)]) + scriptPubKey) if input_index == 0 else b'\x00'
    tx += struct.pack('<I', 0xffffffff)  # sequence
    
    # Input 1
    tx += prev_txid2 + struct.pack('<I', 1)  # txid + vout
    tx += (bytes([len(scriptPubKey)]) + scriptPubKey) if input_index == 1 else b'\x00'
    tx += struct.pack('<I', 0xffffffff)  # sequence
    
    tx += b'\x01'  # output count
    tx += out_value + bytes([len(out_script)]) + out_script
    tx += struct.pack('<I', 0)  # locktime
    tx += struct.pack('<I', 1)  # SIGHASH_ALL
    
    return tx

z1 = int.from_bytes(dsha256(build_sighash(0)), 'big')
z2 = int.from_bytes(dsha256(build_sighash(1)), 'big')

k = ((z1 - z2) * inverse_mod((s1 - s2) % n, n)) % n

d = ((s1 * k - z1) * inverse_mod(r, n)) % n

print(f"Recovered private key: {hex(d)}")

# Decrypt using private key as OTP
priv_bytes = d.to_bytes(32, 'big')
decrypted = bytes(a ^ b for a, b in zip(encrypted, priv_bytes))

print(f"Decrypted (hex): {decrypted.hex()}")
print(f"\nFirst 16: {decrypted[:16].hex()}")