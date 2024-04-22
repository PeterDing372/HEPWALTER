from BPFGrep_stdout import BPFGrep
import subprocess
import time

def run_bpftrace_for_duration(bpffile="final_run.bt"):
    try:
        # Run the BPFtrace script using timeout command
        print("start")
        start_time = time.time()
        command = f"sudo bpftrace {bpffile}"
        BPFGrepObj = BPFGrep(command, verbose=True)
        print("read_one_arg")
        BPFGrepObj.read_one_arg()
        return "regular done"

        # # Read and print output line by line
        # for i, line in enumerate(process.stdout):
        #     # get a new argument info

        #     if time.time() - start_time > duration:
        #         process.terminate()
        #         return f"terminated after {duration} seconds"

        # # Wait for the process to complete or timeout
        # try:
        #     process.wait(timeout=duration)
        # except subprocess.TimeoutExpired:
        #     # If timeout occurs, kill the process
        #     process.terminate()
        #     return f"Execution terminated after {duration} seconds."

        # # Capture stderr if there's any error
        # stderr_output = process.stderr.read().strip()
        # if stderr_output:
        #     return f"Error: {stderr_output}"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    output = run_bpftrace_for_duration()
    print("Output:")
    print(output)


if __name__ == "__main__":
    main()






