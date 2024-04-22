import sys
import subprocess
from ArgClass import ArgClass

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
            print("verify")
            self.verify_initial_output()
        except Exception as e:
            print("Failed to start subprocess:", str(e))
            sys.exit(1)
        # Define all argument attributes
        self.args = {
                "sArg0": ArgClass(),
                "sArg0": ArgClass(),
                "sArg2": ArgClass(),
                "sArg3": ArgClass(),
                "sArg4": ArgClass(),
                "sArg5": ArgClass(),
                "sRetVal": ArgClass(),
                "dArg0": ArgClass(),
                "dArg1": ArgClass(),
                "dArg2": ArgClass(),
                "dArg3": ArgClass(),
                "dArg4": ArgClass(),
                "dArg5": ArgClass(),
                "dRetval": ArgClass()
        }

    def verify_initial_output(self):
        """Reads the first line of output from the subprocess 
            and verifies it is \"Attaching 4 probes...\""""
        try:
            # Read the first line from the output
            initial_output = self.stream.readline()
            if self.verbose:
                print(f"Initial output: {initial_output}")
            # Check if the output matches the expected string
            if "Attaching 4 probes..." not in initial_output:
                error_message = f"Unexpected initial output. Expected 'Attaching 4 probes...', got '{initial_output}'"
                print(error_message)
                # raise ValueError(error_message)
        except ValueError as e:
            print(f"Error: {e}")
            self.cleanup()
            sys.exit(1)

    def cleanup(self):
        if self.process:
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.terminate()  # Ensure the process is terminated
            self.process.wait()  # Wait for the process to terminate

    def __del__(self):
        # Ensure to close the subprocess and its streams
        if self.process:
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()  # Wait for the process to terminate

    def read_one_cluster(self):
        """
        Read one cluster of argument information
        """
        while True:
            label, buffer_content, ptr_addr = self.read_one_arg()
            if (label == "sArg0"):
                self.clear()
        # TODO
    
    #
    def clear():
        """
        Clears all ArgClass attributes one cluster of argument information
        """
        return; 



    def read_one_arg(self):
        self._print("---------- start one set of read ----------")
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
        self._print("arg type: " + arg_type)
        return arg_type

    def read_arg_ptr(self):
        arg_ptr = ""
        while True:
            ch = self.stream.read(1)
            if ch == '\n' or not ch:
                break
            arg_ptr += ch
        self._print("arg ptr: "+ arg_ptr)
        return self.to_int(arg_ptr)

    def to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError:
            self._print(f"Invalid argument: {input_str}")
            return 0

    def read_buffer_content(self):
        self._print("read buffer content:")
        buffer_content = ""
        last13_chars = ""
        max_chars = 14
        count = 0

        while True:
            count+=1
            ch = self.stream.read(1)
            if not ch:
                break
            buffer_content += ch
            last13_chars += ch
            # print(f"{last13_chars} {count}")
            # print(f"{ch}")

            if len(last13_chars) > max_chars:
                last13_chars = last13_chars[1:]

            if self.is_buffer_end(last13_chars):
                break
        buffer_content = self.clean_tail(buffer_content, max_chars)
        self._print(buffer_content)
        return buffer_content

    def is_buffer_end(self, input_str):
        return input_str == "**HEPWALTER***"

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
