with open('melding.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

def decrypt_with_step(ciphertext, step):
    decrypted_text = ""
    for i in range(step):
        decrypted_text += ciphertext[i::step]
    return decrypted_text

for step in range(1, 500):
    decrypted_message = decrypt_with_step(encrypted_text, step)
    if decrypted_message.startswith("pst{"):
        print(f"Step {step}: {decrypted_message[:50]}")
