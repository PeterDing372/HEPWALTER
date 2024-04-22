from BPFGrep_stdout import BPFGrep
import time

def run_bpftrace_for_duration(bpffile="final_run.bt"):
    try:
        # Run the BPFtrace script using timeout command
        print("start")
        # start_time = time.time()
        command = f"sudo bpftrace {bpffile}"
        BPFGrepObj = BPFGrep(command, verbose=False)
        print("start read")
        for i in range(100):
            BPFGrepObj.read_one_cluster()
        for item in BPFGrepObj.divergenceList:
            print(f"max: {item[0]} avg : {item[1]}")
        print(f"total clusters captured: {len(BPFGrepObj.divergenceList)}" )
        
        return "done"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    output = run_bpftrace_for_duration()
    print("Output:")
    print(output)


if __name__ == "__main__":
    main()






