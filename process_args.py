# Define the file path
file_path = 'test.txt'


def read_arg(file):
    char = None
    while char != ':':
        char = file.read(1)
        print(char)
    print("end ptr addr")





def main():
    # Your code here
    # Open the file in read mode
    with open(file_path, 'r') as file:
        read_arg(file)
        # while True:
            # # Read a single character
            # char = file.read(1)
            # # If char is an empty string, end of file has been reached
            # if not char:
            #     break
            # # Process the character (for now, just print it)
            # print(char, end='')

    # Optionally, add a new line at the end for formatting if printing
    print()

if __name__ == "__main__":
    main()



