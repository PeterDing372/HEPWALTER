import sys
import subprocess
import time
import math
from ArgClass import ArgClass

class BPFGrep:
    
    def __init__(self, command=None, verbose=False, useFile=False, fileName=None):
        self.verbose = verbose  # Class attribute to control printing
        self.max_til_now = 0
        self.divergenceList = []
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
        
        if (useFile):
            try:
                self.stream = open(fileName, 'r')
            except Exception as e:
                print("Failed to open file:", str(e))
                sys.exit(1)
        else:
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
        self.clear()
        self.verify_initial_output()


        self.align_cluster()

    def terminate_process(self):
        self.process.terminate()
 
        

    def verify_initial_output(self):
        """Reads the first line of output from the subprocess 
            and verifies it is \"Attaching 4 probes...\""""
        self._print("verifying...")
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
    
    def run_for_duration():
        # TODO
        return 
    

    def read_one_cluster(self):
        # error reporting
        
        if(self.ARGs["sArg0"].get_valid() == False):
            print("[read_one_cluster]: Wrong inital status")
            print("[read_one_cluster]: Re-aligning...")
            self.align_cluster()
        self._read_one_cluster()
        return time.time()

    def _read_one_cluster(self):
        """
        Read one cluster of argument information
        """
        if (self.ARGs["sArg0"].get_valid() == False and self.ARGs["sArg1"].get_valid() == True):
            print("[read_one_cluster]: entered with wrong alignment")
        while True:
            label, buffer_content, ptr_addr = self.read_one_arg()
            if (label == None):
                self.clear()
                break
            if (label not in self.ARGs):
                print(f"unknown argument label: {label}")
                if("Lost" in label):
                    self.clear()
                    break
                sys.exit(1)
            if (label == "sArg0"):
                self.report()
                self.clear()
                self.ARGs[label].update(label, buffer_content, ptr_addr, True) 

                break; 
            self.ARGs[label].update(label, buffer_content, ptr_addr, True) 
    
    

    def report(self):
        div_values = self.compare_all_buff()
        max_val, avg_val = self.find_max_avg(div_values)
        
        self.max_til_now = max(max_val, self.max_til_now)
        print(f"{max_val=} {avg_val=} {self.max_til_now=}")
        self.divergenceList.append((max_val, avg_val))
    
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
        Compare all buff content on only valid content: 1. Non-zero, 2. Striped 3. Valid
        returns: an list of tuples containing (max, avg) pairs of divergence length

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
                
                pointers_different = arg_i.ptr_addr != arg_j.ptr_addr
                if(pointers_different and 
                   arg_i.get_valid() and arg_j.get_valid()
                    and self.not_zero_string(arg_i.buffer_content) and self.not_zero_string(arg_j.buffer_content)):
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
        if (label == None or ptr_addr == None or buffer_content == None):
            return None, None, None
        else:
            return label, buffer_content, ptr_addr

    # ---------- Helper Functions Below ----------
    def lastNchar(self, str, ch, N):
        str += ch
        if len(str) > N:
                str = str[1:]
        return str


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
        last14_chars = ""
        last4_chars = ""
        max_chars = 14
        count = 0
        failed = False  

        while True:
            count+=1
            ch = self.stream.read(1)
            if not ch:
                break
            buffer_content += ch
            last14_chars = self.lastNchar(last14_chars, ch, 14)
            last4_chars = self.lastNchar(last4_chars, ch, 4)
            # last14_chars += ch
            # if len(last14_chars) > max_chars:
            #     last14_chars = last14_chars[1:]
            # print(f"{last14_chars} {count}")
            # print(f"{ch}")
            if (last4_chars == "Lost"):
                # discard the cluster
                failed = True
                break

            if self.is_buffer_end(last14_chars):
                self.stream.read(1)
                break
        buffer_content = self.clean_tail(buffer_content, max_chars)
        buffer_content = self.strip_string(buffer_content)
        self._print(buffer_content)
        if (failed):
            return None
        else: 
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

    def not_zero_string(self, str):
        for char in str:
            if char != '0':
                return True
        return False
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
