def crypt(bitstream, key, size, g=3):
    k = size - 1
    mask = (1 << size) - 1
    for b in bitstream:
        key = (g * key) & mask
        yield (key >> k) ^ b

def try_key_segment(segment_bits, known_plaintext, known_ciphertext, size, start_index):
    segment_size = len(segment_bits)
    mask = (1 << size) - 1
    max_value = (1 << segment_size) - 1

    for value in range(max_value + 1):
        key_segment = value << (size - segment_size - start_index)
        full_key = key_segment
        match = True

        for i in range(len(known_plaintext)):
            encrypted_bit = next(crypt([known_plaintext[i]], full_key, size))
            if encrypted_bit != known_ciphertext[i]:
                match = False
                break

        if match:
            return [int(b) for b in format(value, f'0{segment_size}b')]

    return [-1] * segment_size  # Return -1 if no match found

# Replace with your actual binary sequences
size = 64
known_plaintext_binary = [0] * 802  # Example plaintext
known_ciphertext_binary = [int(bit) for bit in "0000011111000010010001100001110010111001111100110010101001000100001101010000100001111001111110111000001100011011111111100110111101110001100100000001110011000010101101110111100000110100011111111110000100001000111000001111110101100001111110000010111111101110001001101110001111111110100100001110000000010111010000001000010011111011000001111000101111111110101111110001111000100011110000111101010001111110011110111111101000101011110011100001110000111110111110001101111011111100001001111100010000000000111000010000011101111110000111111110110000000110001000000000111110001100111111111111111100011100100000001110101111000001111001010001000000011001111010110110011110001111110111111000100001000001100111011111001011110000011001100000111011000000110011011000111100000001111000100011001111011110010011001000111111111010111111100111010101001110101000010111001011110111101000110001111000000000000111111011001110101111000000111000111001100111110010000000111100011100001110100011000000"]

# Try deducing the first few bits of the key
segment_size = 5  # Number of bits to attempt to deduce at once
deduced_key_bits = try_key_segment([-1] * segment_size, known_plaintext_binary, known_ciphertext_binary, size, 0)
print("Deduced Key Segment:", deduced_key_bits)
