#include "BPFGrep.h"
#define BUFFEREND "**HELALTER***"
#include <iostream>


BPFGrep::BPFGrep(const std::string& filename) {
    file.open(filename);
    if (!file.is_open()) {
        std::cerr << "Unable to open file: " << filename << std::endl;
    }
}

BPFGrep::~BPFGrep() {
    if (file.is_open()) {
        file.close();
    }
}

std::string BPFGrep::readArgLabel() {
    char ch = '\0';
    std::string arg_type = "";

    if (file.is_open()) {
        while (ch != ':' && file.get(ch)) {
            arg_type += ch;
        }
        std::cout << arg_type << std::endl;
    }
    arg_type.resize(arg_type.size() - 1);
    return arg_type;

}

size_t BPFGrep::readArgPtr() {
    char ch = '\0';
    std::string arg_ptr = "";

    if (file.is_open()) {
        while (ch != '\n' && file.get(ch)) {
            arg_ptr += ch;
        }
        std::cout << arg_ptr << std::endl;
    }
    return toInt(arg_ptr);
    
}
size_t BPFGrep::toInt(std::string input) {
    size_t num = 0;
    try {
        num = std::stoi(input);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Invalid argument: " << input << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Out of range: " << e.what() << std::endl;
    }
    return num;
}


std::string BPFGrep::readBufferContent() {
    char ch = '\0';
    std::string buffer_content = "";
    std::string last13Chars;
    const size_t maxChars = 13;

    if (file.is_open()) {
        while (file.get(ch)) {
            buffer_content += ch;
            last13Chars += ch;

            if (last13Chars.size() > maxChars) {
                last13Chars.erase(0, 1);
            }
            if (isBufferEnd(last13Chars)) {
                break;
            }
        }
        cleanTail(buffer_content);
        std::cout << buffer_content << std::endl;
    }
    return buffer_content;

}

void BPFGrep::readOneArg(std::string &label, std::string& bufferContent, int& ptrAddr) {
    // NOTE: the function call procedure needs to be in this order
    label = readArgLabel();
    ptrAddr = readArgPtr();
    bufferContent = readBufferContent();

}

bool BPFGrep::isBufferEnd(const std::string& input) const {
    return input == BUFFEREND;
}

void BPFGrep::cleanTail(std::string& input, const int numCharsToRemove) {
    if (input.size() >= numCharsToRemove) {
        input.resize(input.size() - numCharsToRemove);
    } else {
        std::cerr << "Error: The string is shorter than 13 characters." << std::endl;
    }
}

