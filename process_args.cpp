#include <iostream>
#include <fstream>
#include <string>
#include <deque>

#define BUFFEREND "**HELALTER***"

using namespace std;
// Reads the argument type. {sArg0, sRetVal, dArg0, dRetVal}
void read_arg_label(std::ifstream& file) {

    char ch = NULL;
    std::string arg_type = "";

    if (file.is_open()) {
        while (ch != ':') {  
            file.get(ch); // Reads one character at a time
            arg_type += ch;
        }
        std::cout << arg_type << std::endl; // end line
    } else {
        std::cout << "Unable to open file" << std::endl;
    }
}

// Reads the pointer address of the argument
void read_arg_ptr(std::ifstream& file) {

    char ch = NULL;
    std::string arg_ptr = "";

    if (file.is_open()) {
        while (ch != '\n') {  
            file.get(ch); // Reads one character at a time
            arg_ptr += ch;
        }
        std::cout << arg_ptr << std::endl; // end line
    } else {
        std::cout << "Unable to open file" << std::endl;
    }
}

bool is_buffer_end(std::string input) {
    return input == BUFFEREND;
}

void clean_tail(std::string& input, const int numCharsToRemove = 13) {

    // Check if the string has at least 13 characters
    if (input.size() >= numCharsToRemove) {
        // Resize the string to its new size, minus the last 13 characters
        input.resize(input.size() - numCharsToRemove);
    } else {
        // Optionally handle the case where the string is shorter than 13 characters
        std::cerr << "Error: The string is shorter than 13 characters." << std::endl;
    }

}


// reads the buffer content
void read_buffer_content(std::ifstream& file) {
    char ch = NULL;
    std::string buffer_content = "";
    std::string last13Chars;
    const size_t maxChars = 13;
     if (file.is_open()) {
        while (true) {
            file.get(ch);
            buffer_content += ch;
            last13Chars += ch;

            // Ensure the string only keeps the last 13 characters
            if (last13Chars.size() > maxChars) {
                // Remove the first character to maintain the length of 13
                last13Chars.erase(0, 1);
            }
            if (is_buffer_end(last13Chars)) {
                break;
            }
        }
        // clean up buffer ending
        clean_tail(buffer_content);
        std::cout << buffer_content << std::endl;
     } else {
        std::cout << "Unable to open file" << std::endl;
     }
}


int main() {
    // cout << is_buffer_end("**HELALTER***") << endl;
    std::ifstream file("test.txt");
    read_arg_label(file);
    read_arg_ptr(file);
    read_buffer_content(file);
    file.close(); // close file  

    return 0;
}
