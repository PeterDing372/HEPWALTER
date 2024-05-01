from BPFGrep import BPFGrep
import time
import subprocess


def run_python_script(python_script_path):
    try:
        # Run the Python script
        subprocess.run(['python3', python_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Python script: {e}")

def run_bpftrace_for_duration(duration, lost_threshold, bpffile="final_run_again.bt"):
    try:
        # Run the BPFtrace script using timeout command
        # start_time = time.time()
        command = f"sudo bpftrace {bpffile}"
        BPFGrepObj = BPFGrep(command, verbose=False)
        print("[main] BPF Object created")
        
        TOTAL_RUN_TIME = duration
        LOSTMAX = lost_threshold
        
        start_time_set = False
        start_time = time.time() + 1000000000000
        current_time = -1
        count_iterations = 0

        while time.time() - start_time < TOTAL_RUN_TIME:
            current_time = BPFGrepObj.read_one_cluster()
            count_iterations+=1
            # print(f"{current_time=}")
            if not start_time_set:
                start_time = current_time; start_time_set=True
            if BPFGrepObj.lostEvents > LOSTMAX: 
                print("[Final] Reached max lost event. Terminating")
                break
                
        BPFGrepObj.process.terminate()
        for item in BPFGrepObj.divergenceList:
            if (item[0] > 0):
                print(f"max: {item[0]} avg : {item[1]}")
        print(f"max of max: {BPFGrepObj.max_til_now}")
        print(f"total clusters captured: {len(BPFGrepObj.divergenceList)} total iterations: {count_iterations}" )
        b_per_c = average_second_values(BPFGrepObj.divergenceList)
        b_per_func = b_per_c*91
        print(f"bytes per function call: {b_per_func}")
        
        return b_per_func, BPFGrepObj.max_til_now
    except Exception as e:
        return f"An error occurred: {e}"
def average_second_values(tuples_list):
    if not tuples_list:
        return None  # Handle empty list scenario

    # Summing up all the second elements from each tuple
    total = sum(tup[1] for tup in tuples_list if len(tup) > 1)

    # Calculating the average
    average = total / len(tuples_list)
    
    return average

   
def main():
    print("[main] Generating .bt files")
    run_python_script("prepare.py")
    iterations = 20
    duration = 5
    lost_threshold = 5
    bytes_per_func = []
    max_of_max = 0
    for i in range (iterations):
        print(f"[main] Starting cluster parsing iteration {i}")
        tmp_avg, tmp_max = run_bpftrace_for_duration(duration, lost_threshold)
        max_of_max = max(max_of_max, tmp_max)
        bytes_per_func.append(tmp_avg)
    average_bpf = sum(bytes_per_func)/len(bytes_per_func)
    print(f"Output: {average_bpf=} {max_of_max=}")


if __name__ == "__main__":
    main()






