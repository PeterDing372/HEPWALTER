#ifndef BPFGREP_H
#define BPFGREP_H

#include <fstream>
#include <string>

class BPFGrep {
public:
    explicit BPFGrep(const std::string& filename);
    ~BPFGrep();

    // reads the arguement label {sArg0, sRetVal, dArg0, dRetVal}
    std::string readArgLabel();
    // Reads the pointer address of the argument
    std::string readArgPtr();
    // reads the buffer content
    std::string readBufferContent();

private:
    std::ifstream file;
    /* Helper functiions */
    bool isBufferEnd(const std::string& input) const;
    void cleanTail(std::string& input, const int numCharsToRemove = 13);
};

#endif // BPFGREP_H
