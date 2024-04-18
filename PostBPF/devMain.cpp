#include "BPFGrep.h"
#include <map>
#include <vector>
#include <iostream>


int main() {
    BPFGrep BPFGrepObj("test.txt");
    // buffMap[buffer content] -> ptr addr
    std::map<std::string, std::vector<int>> buffMap;
    const int numElements = 3;
    for (int i = 0; i < numElements; i++) {
        std::string label, bufferContent;
        int ptrAddr;
        BPFGrepObj.readOneArg(label, bufferContent, ptrAddr);
        buffMap[bufferContent].push_back(ptrAddr);
        
        // if (buffMap.find(bufferContent) != buffMap.end()) {
        //     buffMap[bufferContent].push_back(ptrAddr);
        // } else {
        //     buffMap[bufferContent] = 
        // }
    }

    // Example of how to print the contents of the map
    for (const auto& pair : buffMap) {
        std::cout << "Buffer Content: " << pair.first << " -> Pointer Addresses: ";
        for (int addr : pair.second) {
            std::cout << addr << " ";
        }
        std::cout << std::endl;
    }


    return 0;
}