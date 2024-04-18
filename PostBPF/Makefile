CXX=g++
CXXFLAGS = -Wall -Wextra -g
OBJECTS = BPFGrep.o

test:
	$(CXX) $(CXXFLAGS) process_args.cpp -o process_args
devMain: devMain.cpp $(OBJECTS)
	$(CXX) $(CXXFLAGS) devMain.cpp $(OBJECTS) -o devMain
main: main.cpp BPFGrep.o
	$(CXX) $(CXXFLAGS) main.cpp $(OBJECTS) -o main.o
BPFGrep.o: BPFGrep.cpp BPFGrep.h
	$(CXX) $(CXXFLAGS) -c BPFGrep.cpp  -o BPFGrep.o

clean:
	rm -rf *.o process_args devMain main

.PHONY: clean