#ifndef BPFGREP_H
#define BPFGREP_H

#include <fstream>
#include <string>


class BPFGrep {
public:
    explicit BPFGrep(const std::string& filename);
    ~BPFGrep();

    
    void readOneArg(std::string &label, std::string& bufferContent, int& ptrAddr);



private:
    std::ifstream file;
    // reads the arguement label {sArg0, sRetVal, dArg0, dRetVal}
    std::string readArgLabel();
    // Reads the pointer address of the argument
    size_t readArgPtr();
    // reads the buffer content
    std::string readBufferContent();
    /* Helper functiions */
    bool isBufferEnd(const std::string& input) const;
    void cleanTail(std::string& input, const int numCharsToRemove = 13);
    size_t toInt(std::string input);
};

#endif // BPFGREP_H
