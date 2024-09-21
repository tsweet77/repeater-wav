#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>
#include <iomanip>
#include <cmath>
#include <stdexcept>
#include <limits>

#if defined(_WIN32) || defined(_WIN64)
#include <conio.h>
#include <windows.h>
#else
#include <termios.h>
#include <unistd.h>
#endif

// Function to check if a file exists and is accessible
bool fileExists(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    return file.good();
}

// Function to read the entire file into a vector of bytes
std::vector<uint8_t> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Error: Unable to open file '" + filename + "'.");
    }
    // Read file into buffer
    std::vector<uint8_t> buffer((std::istreambuf_iterator<char>(file)),
                                 std::istreambuf_iterator<char>());
    return buffer;
}

// Function to check system endianness
bool isLittleEndian() {
    uint16_t number = 1;
    return *(reinterpret_cast<uint8_t*>(&number)) == 1;
}

// Function to write the WAV header
void writeWAVHeader(std::ofstream& outFile, uint32_t sampleRate, uint16_t bitsPerSample,
                   uint16_t numChannels, uint32_t numSamples) {
    uint32_t byteRate = sampleRate * numChannels * bitsPerSample / 8;
    uint16_t blockAlign = numChannels * bitsPerSample / 8;
    uint32_t subchunk2Size = numSamples * numChannels * bitsPerSample / 8;
    uint32_t chunkSize = 36 + subchunk2Size;

    // Debug: Print header values
    std::cout << "\nWriting WAV Header:\n";
    std::cout << "Chunk Size: " << chunkSize << "\n";
    std::cout << "Subchunk1 Size: 16\n";
    std::cout << "Audio Format: " << 3 << " (IEEE Float)\n";
    std::cout << "Num Channels: " << numChannels << "\n";
    std::cout << "Sample Rate: " << sampleRate << "\n";
    std::cout << "Byte Rate: " << byteRate << "\n";
    std::cout << "Block Align: " << blockAlign << "\n";
    std::cout << "Bits Per Sample: " << bitsPerSample << "\n";
    std::cout << "Subchunk2 Size: " << subchunk2Size << "\n";

    // RIFF header
    outFile.write("RIFF", 4);
    outFile.write(reinterpret_cast<const char*>(&chunkSize), 4);
    outFile.write("WAVE", 4);

    // fmt subchunk
    outFile.write("fmt ", 4);
    uint32_t subchunk1Size = 16; // PCM or IEEE Float
    outFile.write(reinterpret_cast<const char*>(&subchunk1Size), 4);
    uint16_t audioFormat = 3; // 3 = IEEE Float
    outFile.write(reinterpret_cast<const char*>(&audioFormat), 2);
    outFile.write(reinterpret_cast<const char*>(&numChannels), 2);
    outFile.write(reinterpret_cast<const char*>(&sampleRate), 4);
    outFile.write(reinterpret_cast<const char*>(&byteRate), 4);
    outFile.write(reinterpret_cast<const char*>(&blockAlign), 2);
    outFile.write(reinterpret_cast<const char*>(&bitsPerSample), 2);

    // data subchunk
    outFile.write("data", 4);
    outFile.write(reinterpret_cast<const char*>(&subchunk2Size), 4);
}

// Function to set terminal to raw mode (Unix)
#ifndef _WIN32
struct termios orig_termios;

void reset_terminal_mode() {
    tcsetattr(0, TCSANOW, &orig_termios);
}

void set_conio_terminal_mode() {
    struct termios new_termios;

    // take two copies - one for now, one for later
    tcgetattr(0, &orig_termios);
    new_termios = orig_termios;

    // disable canonical mode and echo
    new_termios.c_lflag &= ~(ICANON | ECHO);

    tcsetattr(0, TCSANOW, &new_termios);
}
#endif

int main() {
    try {
        // Check system endianness
        if (!isLittleEndian()) {
            std::cerr << "Error: System is not little-endian. WAV files require little-endian byte order.\n";
            return 1;
        }

        std::string input;
        std::cout << "Enter intention or filename: ";
        std::getline(std::cin, input);

        std::vector<uint8_t> dataBytes;

        // Check if input is a filename
        if (fileExists(input)) {
            dataBytes = readFile(input);
            std::cout << "Reading data from file: " << input << "\n";
        } else {
            // Use input text as bytes (UTF-8)
            dataBytes.assign(input.begin(), input.end());
            std::cout << "Using entered text as input.\n";
        }

        if (dataBytes.empty()) {
            std::cerr << "Error: No data to process.\n";
            return 1;
        }

        // Define prompts
        std::string freqPrompt = "Enter frequency (Hz): ";
        std::string repPrompt = "Enter number of repetitions: ";

        // Variables to store frequency and repetition inputs
        std::string freqInput = "";
        double frequency = 25000.0; // Default frequency

        std::string repInput = "";
        int repetitions = 0;

        // Variables for WAV calculations
        uint32_t sampleRate = 96000; // Set to 96000 Hz
        uint16_t bitsPerSample = 32; // 32-bit float
        uint16_t numChannels = 1; // Mono

        // Variables to track previous line length for clearing
        size_t prevLineLength = 0;

#if defined(_WIN32) || defined(_WIN64)
        // Windows

        // --- Frequency Input ---
        std::cout << freqPrompt;
        bool freqEntered = false;
        while (!freqEntered) {
            if (_kbhit()) {
                char ch = _getch();
                if (ch == '\r') { // Enter key
                    if (freqInput.empty()) {
                        std::cerr << "\nError: Frequency cannot be empty.\n";
                        return 1;
                    }
                    try {
                        frequency = std::stod(freqInput);
                        if (frequency <= 0.0) {
                            std::cerr << "\nError: Frequency must be a positive number.\n";
                            return 1;
                        }
                        freqEntered = true;
                    }
                    catch (...) {
                        std::cerr << "\nError: Invalid frequency input.\n";
                        return 1;
                    }
                }
                else if (ch == '\b') { // Backspace
                    if (!freqInput.empty()) {
                        freqInput.pop_back();
                        // Handle backspace in console
                        std::cout << "\b \b";
                    }
                }
                else if (isdigit(ch) || ch == '.') {
                    // Allow only one decimal point
                    if (ch == '.' && freqInput.find('.') != std::string::npos) {
                        // Ignore additional decimal points
                        continue;
                    }
                    freqInput += ch;
                    std::cout << ch;
                }
                // Optional: You can add more validation or feedback here
            }
        }

        // --- Repetition Input ---
        std::cout << "\n" << repPrompt;

        while (true) {
            if (_kbhit()) {
                char ch = _getch();
                if (ch == '\r') { // Enter key
                    break;
                }
                else if (ch == '\b') { // Backspace
                    if (!repInput.empty()) {
                        repInput.pop_back();
                        // Handle backspace in console
                        std::cout << "\b \b";
                    }
                }
                else if (isdigit(ch)) {
                    repInput += ch;
                    std::cout << ch;
                }
                // Calculate repetitions
                repetitions = repInput.empty() ? 0 : std::stoi(repInput);
                // Calculate file size and duration
                std::string status;
                if (repetitions > 0) {
                    // Each byte is one sample
                    uint32_t numSamples = static_cast<uint32_t>(dataBytes.size()) * repetitions;
                    uint32_t dataChunkSize = numSamples * numChannels * bitsPerSample / 8;
                    uint32_t totalSizeBytes = 44 + dataChunkSize; // WAV header is 44 bytes

                    // Calculate duration
                    float durationSeconds = static_cast<float>(numSamples) / sampleRate;

                    // Calculate size in kB, MB, GB
                    double size = static_cast<double>(totalSizeBytes);
                    std::string sizeUnit = "bytes";
                    if (size >= 1e9) {
                        size /= 1e9;
                        sizeUnit = "GB";
                    }
                    else if (size >= 1e6) {
                        size /= 1e6;
                        sizeUnit = "MB";
                    }
                    else if (size >= 1e3) {
                        size /= 1e3;
                        sizeUnit = "kB";
                    }

                    // Calculate duration string
                    std::string durationStr;
                    if (durationSeconds >= 60.0f) {
                        int minutes = static_cast<int>(durationSeconds) / 60;
                        float seconds = durationSeconds - minutes * 60;
                        durationStr = std::to_string(minutes) + " min " + std::to_string(seconds) + " sec        ";
                    }
                    else if (durationSeconds >= 1.0f) {
                        durationStr = std::to_string(durationSeconds) + " sec        ";
                    }
                    else {
                        int milliseconds = static_cast<int>(durationSeconds * 1000);
                        durationStr = std::to_string(milliseconds) + " ms        ";
                    }

                    // Construct status string
                    status = "Size: " + std::to_string(size).substr(0, 5) + " " + sizeUnit +
                             " | Duration: " + durationStr;
                }
                else {
                    status = "Size: N/A | Duration: N/A";
                }

                // Construct the full line
                std::string fullLine = repPrompt + repInput + " | " + status;

                // Calculate spaces needed to clear previous status
                size_t currentLineLength = fullLine.length();
                size_t clearLength = (prevLineLength > currentLineLength) ? (prevLineLength - currentLineLength) : 0;

                // Move cursor to start, print the full line, and clear the remaining part
                std::cout << "\r" << fullLine;
                if (clearLength > 0) {
                    std::cout << std::string(clearLength, ' ');
                }
                std::cout << std::flush;

                // Update previous line length
                prevLineLength = fullLine.length();
            }
        }

#else
        // Unix/Linux

        // --- Frequency Input ---
        std::cout << freqPrompt;
        set_conio_terminal_mode();
        bool freqEntered = false;
        while (!freqEntered) {
            char ch;
            ssize_t n = read(STDIN_FILENO, &ch, 1);
            if (n > 0) {
                if (ch == '\n' || ch == '\r') { // Enter key
                    if (freqInput.empty()) {
                        std::cerr << "\nError: Frequency cannot be empty.\n";
                        reset_terminal_mode();
                        return 1;
                    }
                    try {
                        frequency = std::stod(freqInput);
                        if (frequency <= 0.0) {
                            std::cerr << "\nError: Frequency must be a positive number.\n";
                            reset_terminal_mode();
                            return 1;
                        }
                        freqEntered = true;
                    }
                    catch (...) {
                        std::cerr << "\nError: Invalid frequency input.\n";
                        reset_terminal_mode();
                        return 1;
                    }
                }
                else if (ch == 127 || ch == '\b') { // Backspace
                    if (!freqInput.empty()) {
                        freqInput.pop_back();
                        // Move cursor back, overwrite with space, move back again
                        std::cout << "\b \b";
                    }
                }
                else if (isdigit(ch) || ch == '.') {
                    // Allow only one decimal point
                    if (ch == '.' && freqInput.find('.') != std::string::npos) {
                        // Ignore additional decimal points
                        continue;
                    }
                    freqInput += ch;
                    std::cout << ch;
                }
                // Optional: You can add more validation or feedback here
            }
        }

        // --- Repetition Input ---
        std::cout << "\n" << repPrompt;

        while (true) {
            char ch;
            ssize_t n = read(STDIN_FILENO, &ch, 1);
            if (n > 0) {
                if (ch == '\n' || ch == '\r') { // Enter key
                    break;
                }
                else if (ch == 127 || ch == '\b') { // Backspace
                    if (!repInput.empty()) {
                        repInput.pop_back();
                        // Move cursor back, overwrite with space, move back again
                        std::cout << "\b \b";
                    }
                }
                else if (isdigit(ch)) {
                    repInput += ch;
                    std::cout << ch;
                }
                // Calculate repetitions
                repetitions = repInput.empty() ? 0 : std::stoi(repInput);
                // Calculate file size and duration
                std::string status;
                if (repetitions > 0) {
                    // Each byte is one sample
                    uint32_t numSamples = static_cast<uint32_t>(dataBytes.size()) * repetitions;
                    uint32_t dataChunkSize = numSamples * numChannels * bitsPerSample / 8;
                    uint32_t totalSizeBytes = 44 + dataChunkSize; // WAV header is 44 bytes

                    // Calculate duration
                    float durationSeconds = static_cast<float>(numSamples) / sampleRate;

                    // Calculate size in kB, MB, GB
                    double size = static_cast<double>(totalSizeBytes);
                    std::string sizeUnit = "bytes";
                    if (size >= 1e9) {
                        size /= 1e9;
                        sizeUnit = "GB";
                    }
                    else if (size >= 1e6) {
                        size /= 1e6;
                        sizeUnit = "MB";
                    }
                    else if (size >= 1e3) {
                        size /= 1e3;
                        sizeUnit = "kB";
                    }

                    // Calculate duration string
                    std::string durationStr;
                    if (durationSeconds >= 60.0f) {
                        int minutes = static_cast<int>(durationSeconds) / 60;
                        float seconds = durationSeconds - minutes * 60;
                        durationStr = std::to_string(minutes) + " min " + std::to_string(seconds) + " sec        ";
                    }
                    else if (durationSeconds >= 1.0f) {
                        durationStr = std::to_string(durationSeconds) + " sec        ";
                    }
                    else {
                        int milliseconds = static_cast<int>(durationSeconds * 1000);
                        durationStr = std::to_string(milliseconds) + " ms        ";
                    }

                    // Construct status string
                    status = "Size: " + std::to_string(size).substr(0, 5) + " " + sizeUnit +
                             " | Duration: " + durationStr;
                }
                else {
                    status = "Size: N/A | Duration: N/A";
                }

                // Construct the full line
                std::string fullLine = repPrompt + repInput + " | " + status;

                // Calculate spaces needed to clear previous status
                size_t currentLineLength = fullLine.length();
                size_t clearLength = (prevLineLength > currentLineLength) ? (prevLineLength - currentLineLength) : 0;

                // Move cursor to start, print the full line, and clear the remaining part
                std::cout << "\r" << fullLine;
                if (clearLength > 0) {
                    std::cout << std::string(clearLength, ' ');
                }
                std::cout << std::flush;

                // Update previous line length
                prevLineLength = fullLine.length();
            }
        }
        reset_terminal_mode();
#endif

        // Validate repetitions
        if (repetitions < 1) {
            std::cerr << "\nError: Number of repetitions must be at least 1.\n";
            return 1;
        }

        // Prepare samples
        // Generate a pure sine wave and modulate its amplitude with data bytes
        // This approach ensures a more "pure" audio signal with fewer unwanted frequencies
        std::vector<float> samples;
        samples.reserve(static_cast<size_t>(dataBytes.size()) * repetitions); // Corrected reservation

        double phase = 0.0;
        double twoPiF = 2.0 * M_PI * frequency;
        double phaseIncrement = twoPiF / sampleRate;

        for (int rep = 0; rep < repetitions; ++rep) {
            for (auto byte : dataBytes) {
                // Normalize byte to [0, 1]
                float amplitude = static_cast<float>(byte) / 255.0f;
                // Generate sine wave sample
                float sample = amplitude * static_cast<float>(sin(phase));
                // Clamp sample to [-1.0, 1.0]
                sample = std::fmax(-1.0f, std::fmin(1.0f, sample));
                samples.push_back(sample);
                phase += phaseIncrement;
                if (phase >= 2.0 * M_PI) {
                    phase -= 2.0 * M_PI;
                }
            }
        }

        uint32_t numSamples = static_cast<uint32_t>(samples.size());

        // Calculate file size
        uint32_t dataChunkSize = numSamples * numChannels * bitsPerSample / 8;
        uint32_t totalSizeBytes = 44 + dataChunkSize; // WAV header is 44 bytes

        // Calculate duration
        float durationSeconds = static_cast<float>(numSamples) / sampleRate;

        // Display final size and duration
        // Calculate size in kB, MB, GB
        double size = static_cast<double>(totalSizeBytes);
        std::string sizeUnit = "bytes";
        if (size >= 1e9) {
            size /= 1e9;
            sizeUnit = "GB";
        }
        else if (size >= 1e6) {
            size /= 1e6;
            sizeUnit = "MB";
        }
        else if (size >= 1e3) {
            size /= 1e3;
            sizeUnit = "kB";
        }

        // Calculate duration string
        std::string durationStr;
        if (durationSeconds >= 60.0f) {
            int minutes = static_cast<int>(durationSeconds) / 60;
            float seconds = durationSeconds - minutes * 60;
            durationStr = std::to_string(minutes) + " min " + std::to_string(seconds) + " sec";
        }
        else if (durationSeconds >= 1.0f) {
            durationStr = std::to_string(durationSeconds) + " sec";
        }
        else {
            int milliseconds = static_cast<int>(durationSeconds * 1000);
            durationStr = std::to_string(milliseconds) + " ms";
        }

        std::cout << "\nFinal output size: " << std::fixed << std::setprecision(2)
                  << size << " " << sizeUnit << "\n";
        std::cout << "Duration of WAV: " << durationStr << "\n";

        // Open output file
        std::ofstream outFile("output.wav", std::ios::binary);
        if (!outFile) {
            std::cerr << "Error: Unable to create 'output.wav'.\n";
            return 1;
        }

        // Write WAV header
        writeWAVHeader(outFile, sampleRate, bitsPerSample, numChannels, numSamples);

        // Write sample data
        outFile.write(reinterpret_cast<const char*>(samples.data()), samples.size() * sizeof(float));

        outFile.close();
        std::cout << "WAV file 'output.wav' has been created successfully.\n";
    }
    catch (const std::exception& ex) {
        std::cerr << ex.what() << "\n";
        return 1;
    }

    // Wait for user to press Enter before closing
    std::cout << "\nPress Enter to exit...";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Clear the input buffer
    std::cin.get(); // Wait for the user to press Enter

    return 0;
}
