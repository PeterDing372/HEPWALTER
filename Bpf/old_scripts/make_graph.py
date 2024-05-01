import matplotlib.pyplot as plt

def create_histogram(file_path):
    # Read the data from the file
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            print(line)
            line = line.split()
            if line:
                data.append((line[0],line[1]))

    # Extract indices and values from the data
    # indices = [int(pair[0]) for pair in data]
    values = [float(pair[1]) for pair in data]
    print(values)

    # Create the histogram
    plt.hist(values, bins=10)  # Adjust the number of bins as needed
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram of Values')
    plt.grid(True)
    plt.show()

# Example usage:
file_path = 'results.txt'  # Replace 'data.txt' with your file path
create_histogram(file_path)
