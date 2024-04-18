class BPFGrep:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = open(self.filename, 'r')
        except Exception as e:
            print(f"Unable to open file: {filename}")
            print(e)

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    def read_arg_label(self):
        arg_type = ""
        while True:
            ch = self.file.read(1)
            if ch == ':' or not ch:
                break
            arg_type += ch
        print(arg_type)
        return arg_type[:-1]

    def read_arg_ptr(self):
        arg_ptr = ""
        while True:
            ch = self.file.read(1)
            if ch == '\n' or not ch:
                break
            arg_ptr += ch
        print(arg_ptr)
        return self.to_int(arg_ptr)

    def to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError as e:
            print(f"Invalid argument: {input_str}")
            return 0

    def read_buffer_content(self):
        buffer_content = ""
        last13_chars = ""
        max_chars = 13

        while True:
            ch = self.file.read(1)
            if not ch:
                break
            buffer_content += ch
            last13_chars += ch

            if len(last13_chars) > max_chars:
                last13_chars = last13_chars[1:]

            if self.is_buffer_end(last13_chars):
                break
        self.clean_tail(buffer_content, max_chars)
        print(buffer_content)
        return buffer_content

    def read_one_arg(self):
        label = self.read_arg_label()
        ptr_addr = self.read_arg_ptr()
        buffer_content = self.read_buffer_content()
        return label, buffer_content, ptr_addr

    def is_buffer_end(self, input_str):
        return input_str == "**HELALTER***"

    def clean_tail(self, input_str, num_chars_to_remove):
        if len(input_str) >= num_chars_to_remove:
            return input_str[:-num_chars_to_remove]
        else:
            print("Error: The string is shorter than 13 characters.")
            return input_str