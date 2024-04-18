CXX=g++
EXECUTABLE = main.o
OBJECTS = BPFGrep.o

test:
	$(CXX) process_args.cpp -o process_args.o
main: main.cpp BPFGrep.o
	$(CXX) main.cpp $(OBJECTS) -o main.o
BPFGrep.o: BPFGrep.cpp BPFGrep.h
	$(CXX) -c BPFGrep.cpp  -o BPFGrep.o

clean:
	rm -rf *.o

PHONY: clean