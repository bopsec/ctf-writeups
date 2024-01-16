def encrypt_decrypt_flag(flag, key):
    # Simple XOR operation for encryption/decryption
    encrypted_decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(flag, key))
    return encrypted_decrypted

# Assuming FLAG is a string
FLAG = "Your_Flag_Here"
encrypted_flag = encrypt_decrypt_flag(FLAG, shared_key)
decrypted_flag = encrypt_decrypt_flag(encrypted_flag, shared_key)

print("Encrypted Flag:", encrypted_flag)
print("Decrypted Flag:", decrypted_flag)
