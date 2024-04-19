from BPFGrep import BPFGrep



def main():
    # Example usage:
    bpfgrep_obj = BPFGrep("test_redundant.txt", verbose=False)
    buff_tuples = [] # (ptr_addr, buffer_content, label)
    num_elements = 6
    # Read through complete file
    for _ in range(num_elements):
        label, buffer_content, ptr_addr = bpfgrep_obj.read_one_arg()
        buff_tuples.append((ptr_addr, buffer_content, label))

    printTupleList(buff_tuples)
    compare_all_buff(buff_tuples)
    

def printTupleList(tuples_list):
    attributes = ["ptr addr", "buffer content", "label"]
    # Print the contents of the map
    for index, tup in enumerate(tuples_list):
        # Convert each tuple to a string and join with commas for nicer output
        print(f"Tuple {index + 1}:")
        for i, item in enumerate(tup):
            print(f"    {attributes[i]}: {item}")
        print()  # Add a blank line for better separation between tuples

# Compare all buff content and 
# returns an index list of tuples containing (i,j) pairs and divergence index
def compare_all_buff(tupleList, div_threshold=3):
    size = len(tupleList)
    for i in range(size):
        for j in range(i + 1, size):
            divege_index = find_divergence(tupleList[i][1], tupleList[j][1])
            if (divege_index >= div_threshold):
                print(f"same buff arg{i} arg{j} div_index: {divege_index}")
                if (tupleList[i][0] != tupleList[j][0]):
                    print("is redundant")

def find_divergence(str1, str2):
    min_length = min(len(str1), len(str2))
    for i in range(min_length):
        if str1[i] != str2[i]:
            return i  
    
    # If no differences were found within the shorter length, 
    # return the length of the shorter string
    return min_length
    

if __name__ == "__main__":
    main()