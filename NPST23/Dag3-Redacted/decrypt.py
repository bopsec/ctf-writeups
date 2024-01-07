from Crypto.Cipher import AES
from Crypto.Util import Counter
import codecs
import binascii

# Parameters
file_path = 'huskeliste.txt.enc'
key_hex = 'dda2846b010a6185b5e76aca4144069f88dc7a6ba49bf128'
iv_rot13 = 'UtgangsVektor123'

# Apply ROT-13 to the IV
iv = codecs.decode(iv_rot13, 'rot_13').encode('utf-8')

# Convert key from hex to bytes
key_bytes = binascii.unhexlify(key_hex)

# Function to decrypt the file using AES-CTR
def decrypt_aes_ctr(file_path, key, iv):
    try:
        # Read the encrypted file
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Create a new AES cipher object in CTR mode
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

        # Decrypt the data
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {e}"

# Attempt to decrypt the file using AES-CTR
decrypted_content = decrypt_aes_ctr(file_path, key_bytes, iv)
decrypted_content
