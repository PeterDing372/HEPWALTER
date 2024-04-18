#include "BPFGrep.h"
// main function for clas tesing
int main() {
    BPFGrep BPFGrep("test.txt");
    BPFGrep.readArgLabel();
    BPFGrep.readArgPtr();
    BPFGrep.readBufferContent();

    return 0;
}