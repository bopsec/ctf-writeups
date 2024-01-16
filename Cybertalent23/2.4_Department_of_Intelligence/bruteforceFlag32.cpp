#include <iostream>
#include <vector>
#include <cstdint>

class Crypt {
public:
    static std::vector<bool> crypt(const std::vector<bool>& bitstream, uint32_t key, int size, int g = 3) {
        std::vector<bool> output;
        int k = size - 1;
        uint32_t mask = (1 << size) - 1;
        for (bool b : bitstream) {
            key = (g * key) & mask;
            output.push_back(((key >> k) ^ b) != 0);
        }
        return output;
    }
};

uint32_t brute_force_key(const std::vector<bool>& known_plaintext, const std::vector<bool>& known_ciphertext, int size) {
    uint64_t progress_interval = 100000000; // Update every 100 million keys tested
    uint64_t mask = (1ULL << size) - 1; // Use 1ULL to ensure 64-bit computation

    for (uint64_t key = 0; key <= mask; ++key) {
        if (key % progress_interval == 0) {
            std::cout << "Tested " << key << " keys..." << std::endl;
        }

        bool key_valid = true;
        uint32_t current_key = static_cast<uint32_t>(key);

        for (size_t i = 0; i < known_plaintext.size(); ++i) {
            bool pt_bit = known_plaintext[i];
            bool encrypted_bit = ((current_key >> (size - 1)) ^ pt_bit) != 0;
            if (encrypted_bit != known_ciphertext[i]) {
                key_valid = false;
                break;
            }
            current_key = (3 * current_key) & static_cast<uint32_t>(mask);
        }

        if (key_valid) {
            return static_cast<uint32_t>(key);
        }
    }
    return 0; // No valid key found
}

int main() {
    const int size = 32;
    std::vector<bool> known_plaintext_binary(802, false);
    std::string known_ciphertext_str = "100000111110000001111001011101110011111100010100000110000110000011101000110110000001101111110001111001111111010000000000001100111011110111100110101111111111110001000000011101100001001110110011000011110111000111110001111111111111111111001111110010111110100000011111111111110000001111110110001100111001111111111111100010000111100110011101110001101101111110000111001010100000100000000001001011111110000011110101000000011010000001110110110001111111110011111110001101000100100000011111001011101111111111110000000000011111100001111101111100101110110111110001010000011001111100011100111000000000011011111001000111010100100000111101110000000001100000000010111111110011000001011010010001111111110111111001110000001111110010000001000001010111011111110000000000101000110000000110011001000110000011011101111101110000000000111010000010110001111111110111101011111000100011110110111111000111110111000100001000010101001111110111011100011100111100101110011101111100000111100001100000000000011101100110111010111110111110110110000001111000000011110001101011111101100010001110100111000000000000111000101111110010010001101100011000000011100110000101110000001111111111100101110111"; // Truncated for brevity
    std::vector<bool> known_ciphertext_binary;

    for (char c : known_ciphertext_str) {
        known_ciphertext_binary.push_back(c == '1');
    }

    uint32_t key = brute_force_key(known_plaintext_binary, known_ciphertext_binary, size);
    if (key != 0) {
        std::cout << "Found key: " << key << std::endl;
    }
    else {
        std::cout << "Key not found." << std::endl;
    }
    return 0;
}

