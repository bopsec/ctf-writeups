from Crypto.Cipher import AES
from base64 import b64decode
import json
import binascii

def xor_hex_strings(hex_str1, hex_str2):
    # Convert hex strings to bytes
    bytes1 = binascii.unhexlify(hex_str1)
    bytes2 = binascii.unhexlify(hex_str2)

    # XOR the bytes
    xor_bytes = bytes(a ^ b for a, b in zip(bytes1, bytes2))

    # Convert back to hex
    return binascii.hexlify(xor_bytes).decode('utf-8')


secret_1 = "980daad49738f76b80c8fafb0673ff1b"
secret_2 = "a3c5a5a81ebc62c6144a9dc1ae5cce11"
secret_3 = "fc78e6fee2138b798e1e51ed15e0a109"

key = binascii.unhexlify(xor_hex_strings(xor_hex_strings(secret_1, secret_2), secret_3))


with open("melding.enc", "rb") as f:
    try:
        data = json.loads(f.read())
        nonce = b64decode(data["nonce"])
        ciphertext = b64decode(data["ciphertext"])
        tag = b64decode(data["tag"])
        cipher = AES.new(key, AES.MODE_GCM, nonce = nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        print("Dekryptert melding: " + plaintext.decode('utf-8'))
    except (ValueError, KeyError):
        print("Oisann, noe gikk galt!")
