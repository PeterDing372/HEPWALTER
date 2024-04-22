class ArgClass:
    def __init__(self, label=None, buffer_content=None, ptr_addr=None):
        self.label = label  # String: Describes the label of the record
        self.buffer_content = buffer_content  # String: Contains the content of the buffer
        self.ptr_addr = ptr_addr  # Integer: Pointer address as an integer
        self._valid = False

    def __str__(self):
        # This method allows the class instance to be printed in a user-friendly format
        return f"ArgClass(Label: {self.label}, Buffer: {self.buffer_content}, Pointer Address: {self.ptr_addr})"
    def update(self, label, buffer_content, ptr_addr, valid):
        self.label = label
        self.buffer_content = buffer_content
        self.ptr_addr = ptr_addr
        self._valid = valid
    def clear(self):
        self.label = None  
        self.buffer_content = None  
        self.ptr_addr = None  
        self._valid = False

    # Valid control
    def set_valid(self):
        self._valid = True
    def unset_valid(self):
        self._valid = False
    def get_valid(self):
        return self._valid


# Example usage of the ArgClass class
if __name__ == "__main__":
    # Creating an instance of ArgClass
    record = ArgClass("FunctionStart", "Here is some buffer content", 0x123456)

    # Printing the instance
    print(record)
