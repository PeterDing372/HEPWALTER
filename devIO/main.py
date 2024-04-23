from BPFGrep_stdout import BPFGrep
import time

def run_bpftrace_for_duration(bpffile="final_run.bt"):
    try:
        # Run the BPFtrace script using timeout command
        print("starting script")
        # start_time = time.time()
        command = f"sudo bpftrace {bpffile}"
        BPFGrepObj = BPFGrep(command, verbose=False)
        print("object created")
        
        TOTAL_RUN_TIME = 100
        
        start_time_set = False
        start_time = time.time() + 1000000000000
        current_time = -1
        count_iterations = 0

        while time.time() - start_time < TOTAL_RUN_TIME:
            current_time = BPFGrepObj.read_one_cluster()
            count_iterations+=1
            print(f"{current_time=}")
            if not start_time_set:
                start_time = current_time; start_time_set=True
                
        BPFGrepObj.process.terminate()
        # for item in BPFGrepObj.divergenceList:
        #     print(f"max: {item[0]} avg : {item[1]}")
        print(f"total clusters captured: {len(BPFGrepObj.divergenceList)} total iterations: {count_iterations}" )
        
        return "done"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    output = run_bpftrace_for_duration()
    print("Output:")
    print(output)


if __name__ == "__main__":
    main()






