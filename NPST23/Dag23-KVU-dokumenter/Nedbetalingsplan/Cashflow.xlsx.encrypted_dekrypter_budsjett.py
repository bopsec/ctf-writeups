from cryptography.fernet import Fernet
import base64

B3 = input("Skriv inn nøkkelord: ")
source_file = 'Cashflow.xlsx.encrypted'
key = base64.urlsafe_b64encode(bytes(B3, encoding='ascii'))

def decrypt_file(encrypted_filename, key):
    cipher_suite = Fernet(key)
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_filename = encrypted_filename.replace('.encrypted', '')
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

decrypt_file(source_file, key)

print(f'{source_file} decrypted.')