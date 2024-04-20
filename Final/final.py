import subprocess
import time

duration = 100  # Duration in seconds

def is_zero_string(line):
    if line[-1] != "h":
        print("SOMETHING IS WRONG in:")
        print(line)
        return False
    line = line.replace('x','')
    line = line.replace('h','')
    line = line.replace('\\','')
    line = line.replace('`','')
    for char in line:
        if char != '0':
            return False
    return True

def parse_ptrs(ptrs):
    overlap = 0
    for item in ptrs:
        if len(ptrs[item]) > 1:
            if(not is_zero_string(item)):
                # print(f"{item} is pointed to by {len(ptrs[item])} and is zero? {is_zero_string(item)} ")
                overlap += len(ptrs[item])-1
    return overlap

def update_ptrs(line, STATE, ptrs, prevs, lineno):

    # print(line)
    start = line.split('\t')[0]
    if (start != 'val' and start != 'ptr'):
        print("Weird line: ", line, " while start was ", start)
        STATE = "READINGPTR"
        return STATE, ptrs, prevs, 0

    overlap = 0
    if ((lineno - 1) % 8) == 0:
        overlap = parse_ptrs(ptrs)
        ptrs = {} 

    data_list = line.split('\t')[1:]
    for i, item in enumerate(data_list):
        if STATE == "READINGPTR":
            prevs.append(item)
        else:
            _list = ptrs.get(item, [])
            _list.append(prevs[i])
            ptrs[item] = _list
    if STATE == "READINGVAL":
        prevs = []

        
    if STATE == "READINGPTR":
        STATE = "READINGVAL"
    elif STATE == "READINGVAL":
        STATE = "READINGPTR"

    return STATE, ptrs, prevs, overlap

def run_python_script(python_script_path):
    try:
        # Run the Python script
        subprocess.run(['python3', python_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Python script: {e}")



def run_bpftrace_for_duration(duration, bpffile="final_run.bt"):
    try:
        prevs = []
        ptrs = {}
        # Run the BPFtrace script using timeout command
        start_time = time.time()
        command = f"sudo bpftrace {bpffile}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        STATE = "start"

        overlap_till_now = 0

        # Read and print output line by line
        for i, line in enumerate(process.stdout):
            STATE, ptrs, prevs, overlap = update_ptrs(line.strip(), STATE, ptrs, prevs, i)
            overlap_till_now += overlap
            if time.time() - start_time > duration:
                print(f"{overlap_till_now=}")
                print(f"avg shared ptrs per call = {overlap_till_now / (i/8)}")
                process.terminate()
                return f"terminated after {duration} seconds"

        # Wait for the process to complete or timeout
        try:
            process.wait(timeout=duration)
        except subprocess.TimeoutExpired:
            # If timeout occurs, kill the process
            process.terminate()
            return f"Execution terminated after {duration} seconds."

        # Capture stderr if there's any error
        stderr_output = process.stderr.read().strip()
        if stderr_output:
            return f"Error: {stderr_output}"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
run_python_script("prepare.py")

output = run_bpftrace_for_duration(duration)
print("Output:")
print(output)
