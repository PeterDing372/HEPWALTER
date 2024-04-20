import sys
import subprocess

class BPFGrep:
    def __init__(self, command, verbose=False):
        self.verbose = verbose  # Class attribute to control printing
        try:
            # Set up the subprocess to execute the command and capture its stdout
            self.process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            self.stream = self.process.stdout
        except Exception as e:
            print("Failed to start subprocess:", str(e))
            sys.exit(1)

    def __del__(self):
        # Ensure to close the subprocess and its streams
        if self.process:
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()  # Wait for the process to terminate

    def read_one_arg(self):
        label = self.read_arg_label()
        ptr_addr = self.read_arg_ptr()
        buffer_content = self.read_buffer_content()
        return label, buffer_content, ptr_addr

    # ---------- Helper Functions Below ----------

    def read_arg_label(self):
        arg_type = ""
        while True:
            ch = self.stream.read(1)
            if ch == ':' or not ch:
                break
            arg_type += ch
        self._print(arg_type)
        return arg_type

    def read_arg_ptr(self):
        arg_ptr = ""
        while True:
            ch = self.stream.read(1)
            if ch == '\n' or not ch:
                break
            arg_ptr += ch
        self._print(arg_ptr)
        return self.to_int(arg_ptr)

    def to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError:
            self._print(f"Invalid argument: {input_str}")
            return 0

    def read_buffer_content(self):
        buffer_content = ""
        last13_chars = ""
        max_chars = 13

        while True:
            ch = self.stream.read(1)
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
