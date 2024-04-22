import sys
import subprocess
from ArgClass import ArgClass

class BPFGrep:
    
    def __init__(self, command, verbose=False):
        self.verbose = verbose  # Class attribute to control printing
        # Define all argument attributes
        self.ARGs = {
                "sArg0": ArgClass(),
                "sArg1": ArgClass(),
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
        self.clear()
        self.divergenceList = []
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
            self._print("verify")
            self.verify_initial_output()
            self.align_cluster()
        except Exception as e:
            print("Failed to start subprocess:", str(e))
            sys.exit(1)
        

    def verify_initial_output(self):
        """Reads the first line of output from the subprocess 
            and verifies it is \"Attaching 4 probes...\""""
        try:
            # Read the first line from the output
            initial_output = self.stream.readline()
            self._print(f"Initial output: {initial_output}")
            # Check if the output matches the expected string
            if "Attaching 4 probes..." not in initial_output:
                error_message = f"Unexpected initial output. Expected 'Attaching 4 probes...', got '{initial_output}'"
                self._print(error_message)
                # raise ValueError(error_message)
        except ValueError as e:
            print(f"Error: {e}")
            self.cleanup()
            sys.exit(1)
    def align_cluster(self):
        """
        Initial alignmeent of the read sequence to start with sArg0
        [Note] this will init the sArg0 object
        """
        while True:
            label, buffer_content, ptr_addr = self.read_one_arg()
            if (label == "sArg0"):
                # clear all argument
                self.clear()
                self.ARGs[label].update(label, buffer_content, ptr_addr, True) 
                self._print("Done alignment")
                break

    def cleanup(self):
        """clean up the pipes and exit"""
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
        # error reporting
        if (self.ARGs["sArg0"].get_valid() == False and self.ARGs["sArg1"].get_valid() == True):
            print("[read_one_cluster]: exit with wrong alignment")
        if(self.ARGs["sArg0"].get_valid() == False):
            print("[read_one_cluster]: entered with wrong inital statue")
        while True:
            label, buffer_content, ptr_addr = self.read_one_arg()
            if (label not in self.ARGs):
                print(f"unknown argument label: {label}")
                sys.exit(1)
            if (label == "sArg0"):
                self.report()
                self.clear()
                self.ARGs[label].update(label, buffer_content, ptr_addr, True) 

                break; 
            self.ARGs[label].update(label, buffer_content, ptr_addr, True) 
    
    

    def report(self):
        div_values = self.compare_all_buff()
        max , avg = self.find_max_avg(div_values)
        self.divergenceList.append((max, avg))
    
    def find_max_avg(self, div_values):
        """
        input: div_values
        return: max, avg
        """
        self._print("Find max avg")
        
        if not div_values:  # Check if the list is empty
            return None, None  # Return None for both max and average if the list is empty
        
        max_value = max(div_values)  # Find the maximum value in the list
        average_value = sum(div_values) / len(div_values)  # Calculate the average value
        return max_value, average_value
    
    
    def compare_all_buff(self):
        """
        Compare all buff content and 
        returns an index list of tuples containing (i,j) pairs and divergence index
        """
        self._print("Compare all buffers")
        div_values = []
        keys = list(self.ARGs.keys())
        self._print(keys)
        num_keys = len(keys)
        for i in range(num_keys):
            for j in range(i + 1, num_keys):
                key_i = keys[i]
                key_j = keys[j]
                arg_i = self.ARGs[key_i]
                arg_j = self.ARGs[key_j]
                if(arg_i.get_valid() and arg_j.get_valid()):
                    div_index = self.find_divergence(arg_i.buffer_content, arg_j.buffer_content)
                    div_values.append(div_index)
        return div_values
    
    def clear(self):
        """
        Clears all ArgClass attributes one cluster of argument information
        """
        # Verify by printing the values
        for key in self.ARGs:
            self.ARGs[key].clear()



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
                self.stream.read(1)
                break
        buffer_content = self.clean_tail(buffer_content, max_chars)
        buffer_content = self.strip_string(buffer_content)
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
        
    def strip_string(self, str):
        str = str.replace('x','')
        str = str.replace('h','')
        str = str.replace('\\','')
        str = str.replace('`','')
        return str

    def is_zero_string(self, str):
        for char in str:
            if char != '0':
                return False
        return True
    def find_divergence(self, str1, str2):
        """
        Finds the divergence index of two strings
        
        return: Index of divergence in strings
        return the length of the shorter string if no differences were found
        """
        self._print("find divergence")
        min_length = min(len(str1), len(str2))
        for i in range(min_length):
            if str1[i] != str2[i]:
                self._print("find divergence done")
                return i  
    
        # If no differences were found within the shorter length, 
        # return the length of the shorter string
        self._print("find divergence done")

        return min_length

    # Private helper method to control printing
    def _print(self, message):
        if self.verbose:
            print(message)
