#include <iostream>
#include <fstream>

void read_arg_label(std::ifstream& file) {
    char ch;

    if (file.is_open()) {
        while (file.get(ch)) {  // Reads one character at a time
            std::cout << ch;
        }
        file.close();
    } else {
        std::cout << "Unable to open file" << std::endl;
    }


}


int main() {
    std::ifstream file("test.txt");
    read_arg_label(file);
    return 0;
}
