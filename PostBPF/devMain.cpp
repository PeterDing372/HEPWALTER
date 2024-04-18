#include "BPFGrep.h"
#include <map>
void add(){

}

int main() {
    // buffMap[buffer content] -> ptr addr
    std::map<std::string, int> buffMap;

    BPFGrep BPFGrep("test.txt");
    BPFGrep.readArgLabel();
    BPFGrep.readArgPtr();
    BPFGrep.readBufferContent();

    return 0;
}