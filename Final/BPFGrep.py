import sys
class BPFGrep:
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose  # Class attribute to control printing
        try:
            self.file = open(self.filename, 'r')
        except Exception as e:
            print(f"Unable to open file: {filename}")
            print(e)
            sys.exit(1)

    def __del__(self):
        if self.file and not self.file.closed:
            self.file.close()

    def read_one_arg(self):
        label = self.read_arg_label()
        ptr_addr = self.read_arg_ptr()
        buffer_content = self.read_buffer_content()
        return label, buffer_content, ptr_addr

    # ---------- Helper Functions Below ----------

    def read_arg_label(self):
        arg_type = ""
        while True:
            ch = self.file.read(1)
            if ch == ':' or not ch:
                break
            arg_type += ch
        self._print(arg_type)
        return arg_type

    def read_arg_ptr(self):
        arg_ptr = ""
        while True:
            ch = self.file.read(1)
            if ch == '\n' or not ch:
                break
            arg_ptr += ch
        self._print(arg_ptr)
        return self.to_int(arg_ptr)

    def to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError as e:
            self._print(f"Invalid argument: {input_str}")
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
        buffer_content = self.clean_tail(buffer_content, max_chars)
        self._print(buffer_content)
        return buffer_content

    def is_buffer_end(self, input_str):
        return input_str == "**HELALTER***"

    def clean_tail(self, input_str, num_chars_to_remove):
        if len(input_str) >= num_chars_to_remove:
            return input_str[:-num_chars_to_remove]
        else:
            self._print("Error: The string is shorter than 13 characters.")
            return input_str

    # Private helper method to control printing
    def _print(self, message):
        if self.verbose:
            print(message)