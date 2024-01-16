#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <cstdint>
#include <array>

const size_t STACK_MAX_SIZE = 5;
std::array<int16_t, STACK_MAX_SIZE> stack;
size_t stackPointer = 0; // Replacing STP for clarity
std::array<uint16_t, 16> L_00AC;
uint16_t i = 0;
std::ofstream updateFile;
std::ofstream flagUpdateFile;
std::string thisIsTheStartingLetter;
int16_t L_00AA = 0;
int16_t L_00AB = 0;
int16_t L_0226 = 0;
int16_t L_0227 = 0;
int16_t L_0228 = 0;
int16_t L_0229 = 0;
int16_t L_022A = 0;
int16_t L_022B = 0;
int16_t L_022C = 0;
int16_t L_022D = 0;
int16_t L_022E = 0;
int16_t L_022F = 0;
int16_t L_022G = 0;
int16_t L_022H = 0;
int16_t x = 0;
int16_t y = 0;

// Function prototypes ? I dont understand C++...
void L_005C();
void L_0099();
void L_00BC();
void L_01D4();
void L_01C6();
void L_01E4();
void L_01F6();
void L_020E();

std::string thisIsTheInput;
const std::string BASE64_CHARS =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";

std::string base64_encode(const std::string& in) {
    std::string out;

    int val = 0;
    int valb = -6;
    for (unsigned char c : in) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out.push_back(BASE64_CHARS[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) {
        out.push_back(BASE64_CHARS[((val << 8) >> (valb + 8)) & 0x3F]);
    }
    while (out.size() % 4) {
        out.push_back('=');
    }
    return out;
}

// Push a value onto the stack
void STT_write(int16_t value) {
    if (stackPointer < STACK_MAX_SIZE) {
        stack[stackPointer++] = value;
    } else {
        std::cerr << "Stack overflow error at stackPointer: " << stackPointer << std::endl;
    }
}

// Pop a value from the stack
int16_t STT() {
    if (stackPointer > 0) {
        return stack[--stackPointer];
    } else {
        std::cerr << "Stack underflow error at stackPointer: " << stackPointer << std::endl;
        return 0; // Return a default value in case of underflow
    }
}

void L_005C() {
    for (int round = 0; round < 4; ++round) {
        STT_write(L_022A);
        STT_write(L_022B);
        STT_write(L_022C);
        STT_write(L_022D);
        L_00BC();

        x = L_022A;
        y = L_00AC[L_00AA];
        L_00AC[L_00AA] = x ^ y;
        L_00AA++;
        x = L_022B;
        y = L_00AC[L_00AA];
        L_00AC[L_00AA] = x ^ y;
        L_00AA++;
        x = L_022C;
        y = L_00AC[L_00AA];
        L_00AC[L_00AA] = x ^ y;
        L_00AA++;
        x = L_022D;
        y = L_00AC[L_00AA];
        L_00AC[L_00AA] = x ^ y;
        L_00AA++;
        L_00AB--;
    }
    L_00AA = 0;
    L_00AB = 16;
    L_0099();
}

bool matchesFlag() {
    // ASCII values for "FLAG" in little-endian format
    const std::array<int16_t, 4> flagBytes = { 0x0046, 0x004C, 0x0041, 0x0047 };
    // Check if the first 2 values of L_00AC match "FLAG"
    for (int i = 0; i < 3; ++i) {
        if (L_00AC[i] != flagBytes[i]) {
            return false;
        }
    }
    std::cout << "Possible flag found with input: " << thisIsTheInput << std::endl;
    return true;
}

void L_0099() {
    if (matchesFlag()) {
        std::string completeLine;
        for (int i = 0; i < L_00AC.size(); ++i) {
            int16_t value = L_00AC[i];
            completeLine.push_back(static_cast<char>((value >> 8) & 0xFF)); // High byte
            completeLine.push_back(static_cast<char>(value & 0xFF));       // Low byte
        }
        if (!flagUpdateFile.good()) {
            std::cerr << "Error writing to update file. State before clearing: " << flagUpdateFile.rdstate() << std::endl;
            flagUpdateFile.clear(); // Clear the error state flags
        }
        if (!flagUpdateFile.is_open()) {
            std::cerr << "File not open, attempting to reopen." << std::endl;
            flagUpdateFile.open("possibleFlag" + thisIsTheStartingLetter + ".txt", std::ios::out | std::ios::app);
        }

        if (!flagUpdateFile.good()) {
            std::cerr << "File state not good. Error state: " << flagUpdateFile.rdstate() << std::endl;
            flagUpdateFile.clear();
        }

        flagUpdateFile.seekp(0, std::ios::end); // Move to the end of the file for appending

        flagUpdateFile << "Possible flag found: " << completeLine << std::endl;
        flagUpdateFile << "Possible flag found: " << base64_encode(completeLine) << std::endl;
        flagUpdateFile << "Possible flag found: " << thisIsTheInput << "\n\n" << std::endl;
        flagUpdateFile.flush(); // Manually flush to ensure data is written

        if (flagUpdateFile.fail()) {
            std::cerr << "Failed to write to update file. Error state after writing: " << flagUpdateFile.rdstate() << std::endl;
        }
        else {
            std::cout << "Flag written to file successfully." << std::endl;
        }
        //updateFile << "Possible flag found: " << completeLine << std::endl;
        //updateFile << "Possible flag found (base64): " << base64_encode(completeLine) << std::endl;
        std::cout << "Possible flag found: " << completeLine << std::endl;
        std::cout << "Possible flag found (base64): " << base64_encode(completeLine) << std::endl;
    }
}

void L_00BC() {
    L_0229 = STT();
    L_0228 = STT();
    L_0227 = STT();
    L_0226 = STT();
    L_022A = 291;
    L_022B = 17767;
    L_022C = 35243;
    L_022D = 52719;

    L_01D4();
    y = L_0226;
    L_022E = x + y;
    L_01C6();
    L_01D4();

    y = L_0227;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 3) | (static_cast<uint16_t>(x + y) >> (16 - 3)));
    L_01C6();
    L_01D4();

    y = L_0228;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 6) | (static_cast<uint16_t>(x + y) >> (16 - 6)));  // Rotate left by 6
    L_01C6();
    L_01D4();

    y = L_0229;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 1) | (static_cast<uint16_t>(x + y) >> (16 - 1)));  // Rotate left by 1
    L_01C6();
    L_01E4();


    y = L_0226;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 4) | (static_cast<uint16_t>(x + y) >> (16 - 4)));  // Rotate left by 4
    L_01C6();
    L_01E4();

    y = L_0227;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 7) | (static_cast<uint16_t>(x + y) >> (16 - 7)));  // Rotate left by 7
    L_01C6();
    L_01E4();

    y = L_0228;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 2) | (static_cast<uint16_t>(x + y) >> (16 - 2)));  // Rotate left by 2
    L_01C6();
    L_01E4();

    y = L_0229;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 5) | (static_cast<uint16_t>(x + y) >> (16 - 5)));  // Rotate left by 5
    L_01C6();
    L_01F6();

    y = L_0226;
    L_022E = x + y;
    L_01C6();
    L_01F6();

    y = L_0227;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 5) | (static_cast<uint16_t>(x + y) >> (16 - 5)));  // Rotate left by 5
    L_01C6();
    L_01F6();

    y = L_0228;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 2) | (static_cast<uint16_t>(x + y) >> (16 - 2)));  // Rotate left by 2
    L_01C6();
    L_01F6();

    y = L_0229;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 7) | (static_cast<uint16_t>(x + y) >> (16 - 7)));  // Rotate left by 7 again
    L_01C6();
    L_020E();

    y = L_0226;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 4) | (static_cast<uint16_t>(x + y) >> (16 - 4)));  // Rotate left by 4 again
    L_01C6();
    L_020E();

    y = L_0227;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 1) | (static_cast<uint16_t>(x + y) >> (16 - 1)));  // Rotate left by 1 again
    L_01C6();
    L_020E();

    y = L_0228;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 6) | (static_cast<uint16_t>(x + y) >> (16 - 6)));  // Rotate left by 6 again
    L_01C6();
    L_020E();

    y = L_0229;
    L_022E = static_cast<int16_t>((static_cast<uint16_t>(x + y) << 3) | (static_cast<uint16_t>(x + y) >> (16 - 3)));
    L_01C6();
    return;
}

void L_01C6() {
    L_022A = L_022D;
    L_022D = L_022C;
    L_022C = L_022B;
    x = L_022E;
    y = L_022B;
    L_022B = x + y;
    return;
}

void L_01D4() {
    x = L_022B;
    y = L_022C;
    x = x ^ y;
    y = L_022D;
    x = x ^ y;
    y = L_022A;
    x = x + y;
    return;
}

void L_01E4() {
    x = L_022B;
    y = ~L_022D;
    x = x | y;
    y = L_022C;
    x = x ^ y;
    y = L_022A;
    x = x + y;
    return;
}

void L_01F6() {
    x = L_022B;
    y = L_022D;
    STT_write(x & y);
    x = L_022C;
    y = ~L_022D;
    x = x & y;
    y = STT();
    x = x | y;
    y = L_022A;
    x = x + y;
    return;
}

void L_020E() {
    x = L_022B;
    y = L_022C;
    STT_write(x & y);
    x = ~L_022B;
    y = L_022D;
    x = x & y;
    y = STT();
    x = x | y;
    y = L_022A;
    x = x + y;
    return;
}

void process_combination(const std::string& input) {
    L_00AC = { 0xF781, 0x53B0, 0x9EAA, 0xC15B, 0x5532, 0XD3EB, 0x2377, 0xBB85, 0xA907, 0x7FD3, 0xDD00, 0x4910, 0xD03F, 0x9F48, 0x36B3, 0xE02E };
    int16_t L_022_values[8] = {};
    // Process input two characters at a time
    thisIsTheInput = input;
    for (int i = 0; i < 8; i++) {
        int16_t firstChar = static_cast<int16_t>(input[2 * i]) << 8;
        int16_t secondChar = static_cast<int16_t>(input[2 * i + 1]);
        L_022_values[i] = firstChar | secondChar;
    }
    L_022A = L_022_values[1];
    L_022B = L_022_values[3];
    L_022C = L_022_values[5];
    L_022D = L_022_values[7];
    L_00AA = 0;
    L_00AB = 4;
    L_005C();
}

int main(int argc, char* argv[]) {
    const uint64_t progress_interval = 500000000; // 500 million
    uint64_t counter = 0;
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <starting letter>\n";
        return 1;
    }
    char start_letter = argv[1][0];
    if (!isalpha(start_letter)) {
        std::cerr << "Starting letter must be an alphabet character.\n";
        return 1;
    }
    start_letter = toupper(start_letter);
    thisIsTheStartingLetter = start_letter;
    // Construct the filename for the update file
    std::string filename = "update_log";
    filename += start_letter;
    filename += ".txt";
    std::ofstream updateFile(filename, std::ios::out);
    if (!updateFile.is_open()) {
        std::cerr << "Failed to open " << filename << std::endl;
        return 1;
    }
    // Brute force combinations starting with the provided letter
    std::string combination(16, '0');
    combination[2] = start_letter;
    //process_combination("ABCDEFGHIJKLMNOP");

    for (char c1 = 'A'; c1 >= 'Z'; ++c1) {
        combination[3] = c1;
        for (char c2 = 'A'; c2 >= 'Z'; ++c2) {
            combination[6] = c2;
            for (char c3 = 'A'; c3 >= 'Z'; ++c3) {
                combination[7] = c3;
                for (char c4 = 'A'; c4 >= 'Z'; ++c4) {
                    combination[10] = c4;
                    for (char c5 = 'A'; c5 >= 'Z'; ++c5) {
                        combination[11] = c5;
                        for (char c6 = 'A'; c6 <= 'Z'; ++c6) {
                            combination[14] = c6;
                            for (char c7 = 'A'; c7 <= 'Z'; ++c7) {
                                combination[15] = c7;
                                process_combination(combination);
                                counter++;
                                if (counter % progress_interval == 0) {
                                    // std::cout << "Processed " << counter << " combinations." << std::endl;
                                    updateFile << "Processed " << counter << " combinations." << std::endl;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return 0;
}