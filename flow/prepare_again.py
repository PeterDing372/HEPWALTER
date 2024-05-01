import sys
import subprocess
import json
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument()


# container_name = "socialNetwork_social-graph-mongod"
#container_name = "socialNetwork_media-frontend"
container_name = "socialNetwork_user-timeline-mongodb"

binary = "/usr/bin/mongod"
# binary = "/usr/local/openresty/nginx/sbin/nginx"
# source unmangled name
Source = "mongo::AuthorizationManagerImpl::isAuthEnabled()"
# dest unmangled name
Dest = "mongo::AuthzSessionExternalStateServerCommon::_checkShouldAllowLocalhost(mongo::OperationContext*)"
#bufflength = 64
bufflength = 32
#ptr_incrementlength = 1
ptr_incrementAmount = bufflength

#Don't modify these names
mangledfilename = "manglednames.txt"
unmangledfilename = "unmangledmanglednames.txt"


import subprocess

def get_container_pid(container_name_partial):
    try:
        # List all running containers
        output = subprocess.check_output(['sudo', 'docker', 'ps', '--format', '{{.Names}}'])
        # Decode the output and split into container names
        container_names = output.decode().strip().split('\n')
        
        # Find matching container names
        matching_containers = [name for name in container_names if container_name_partial in name]
        
        if not matching_containers:
            print("No containers found with the partial name provided.")
            return None
        
        # Assuming you want PIDs of all matching containers
        pids = []
        for container in matching_containers:
            # Get the PID of each matching container
            pid_output = subprocess.check_output(['sudo', 'docker', 'inspect', '-f', '{{.State.Pid}}', container])
            pid = int(pid_output.decode().strip())
            pids.append((container, pid))
        
        for cont, pid in pids:
            print(f"The pid for {cont} is: {pid}")
        
        return pids[0][1]

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None



pid = get_container_pid(container_name)

print(f"container name is {container_name} and PID is {pid}")


def create_objdumps(path_to_binary):

    unmangled = subprocess.check_output(['sudo', 'objdump', '-CT', path_to_binary])
    mangled = subprocess.check_output(['sudo', 'objdump', '-T', path_to_binary])

    return unmangled.decode('utf-8'), mangled.decode('utf-8')

def find_mangled_name(objdump_T_output, objdump_CT_output, unmangled_name):
    mangled_name = None
    # Parse objdump -CT output to find addresses
    address = ""

    candidate_unmangled_name = ""
    
    for line in objdump_CT_output.split('\n'):
        if unmangled_name in line:
            unmangled_name_in_line = line.split(' ')[-1]
            if not candidate_unmangled_name or len(candidate_unmangled_name) > len(unmangled_name_in_line):
                address = line.split(' ')[0]
                candidate_unmangled_name = unmangled_name_in_line

    if not address:
        print("NOT FOUND!!")
        return ""



    candidate_mangled_names = []

    for line in objdump_T_output.split('\n'):
        mangled_address = line.split(' ')[0]
        if mangled_address == address:
            # print(line)
            candidate_mangled_names.append(line.split(' ')[-1])


    if candidate_mangled_names:
        print("mangled name: ", min(candidate_mangled_names, key=len))
        print("unmanged name: ", candidate_unmangled_name)
        return min(candidate_mangled_names, key=len)


    print("Not found")
    return ""

def replace_in_file(file_path, desired_file_name, replace, with_):
    try:
        # Open original file for reading
        with open(file_path, 'r') as original_file:
            # Read the contents of the original file
            contents = original_file.read()

        # Replace occurrences of 'replace' with 'with_'
        modified_contents = contents.replace(replace, with_)

        # Create the new file with replaced content
        with open(desired_file_name, 'w') as new_file:
            new_file.write(modified_contents)

        print(f"Replacement completed. New file '{desired_file_name}' created.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def args_string(type_args ,ptrIncrementLength, incrementAmount):
    
    final_string = ""
    num_args = 6
    

    for arg_num in range(num_args):
        currPtrIncrementLength = ptrIncrementLength
        curr_string = ""
        increment = 0
        if type_args.lower() == "source":
            if currPtrIncrementLength <= 0:
                curr_string += "\tprintf(\"sArgJESSE:%zu\\n%r**HEPWALTER***\\n\", argJESSE, buf(argJESSE, HANK));\n\n"
            else:
                curr_string += "\tprintf(\"sArgJESSE:%zu\\n%r\", argJESSE, buf(argJESSE, HANK));\n"
        elif type_args.lower() == "destination":
            if currPtrIncrementLength <= 0:
                curr_string += "\tprintf(\"dArgJESSE:%zu\\n%r**HEPWALTER***\\n\", argJESSE, buf(argJESSE, HANK));\n\n"
            else:
                curr_string += "\tprintf(\"dArgJESSE:%zu\\n%r\", argJESSE, buf(argJESSE, HANK));\n"


        while(currPtrIncrementLength):
            increment += incrementAmount
            if currPtrIncrementLength == 1:
                #if type_args.lower() == "source":
                curr_string += "\tprintf(\"%r**HEPWALTER***\\n\", buf(argJESSE+" + str(increment) + ", HANK));\n\n"
            else:
                curr_string += "\tprintf(\"%r\", buf(argJESSE+" + str(increment) + ", HANK));\n"
            

            currPtrIncrementLength -= 1

        final_string += curr_string
        final_string = final_string.replace("JESSE", str(arg_num))
        final_string = final_string.replace("HANK", str(bufflength))


    return final_string

def retval_string(type_args ,ptrIncrementLength, incrementAmount):
    
    final_string = ""
    

    currPtrIncrementLength = ptrIncrementLength
    curr_string = ""
    increment = 0
    if type_args.lower() == "source":
        if currPtrIncrementLength <= 0:
            final_string += "\tprintf(\"sRetVal:%zu\\n%r**HEPWALTER***\\n\", retval, buf(retval, HANK));\n\n"
        else:
            curr_string += "\tprintf(\"sRetVal:%zu\\n%r\", retval, buf(retval, HANK));\n"
    elif type_args.lower() == "destination":
        if currPtrIncrementLength <= 0:
            final_string += "\tprintf(\"dRetval:%zu\\n%r**HEPWALTER***\\n\", retval, buf(retval, HANK));\n\n"
        else:
            curr_string += "\tprintf(\"dRetval:%zu\\n%r\", retval, buf(retval, HANK));\n"


    while(currPtrIncrementLength):
        increment += incrementAmount
        
        if currPtrIncrementLength == 1:
            #if type_args.lower() == "source":
            curr_string += "\tprintf(\"%r**HEPWALTER***\\n\", buf(retval+" + str(increment) + ", HANK));\n\n"
        else:
            curr_string += "\tprintf(\"%r\", buf(retval+" + str(increment) + ", HANK));\n"
        
        
        currPtrIncrementLength -= 1

        final_string += curr_string
        curr_string = ""
        

    final_string = final_string.replace("HANK", str(bufflength))
    

    return final_string
            

            
        




if __name__ == "__main__":

    path_to_binary = f"/proc/{pid}/root/{binary}"
    # path_to_binary = "/proc/449844/root/usr/local/openresty/nginx/sbin/nginx"

    objdump_CT_output, objdump_T_output = create_objdumps(path_to_binary)

    #with open(mangledfilename, "r") as f:
    #    objdump_T_output = f.read()

    #with open(unmangledfilename, "r") as f:
    #    objdump_CT_output = f.read()

    mangled_source_name = find_mangled_name(objdump_T_output, objdump_CT_output, Source)
    mangled_dest_name = find_mangled_name(objdump_T_output, objdump_CT_output, Dest)
    replace_in_file("final_template_again.bt", "final_run_again.bt", "SOURCE", mangled_source_name)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "DEST", mangled_dest_name)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "binary", binary)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "PID", str(pid))
    replace_in_file("final_run_again.bt", "final_run_again.bt","BUFFLENGTH", str(bufflength))

    if len(sys.argv) > 1:
        num_prints = int(sys.argv[1])
    else:
        num_prints = 0
    source_args_string = args_string("source", num_prints, ptr_incrementAmount)
    destination_args_string = args_string("destination", num_prints, ptr_incrementAmount)
    source_retval_string = retval_string("source", num_prints, ptr_incrementAmount)
    destination_retval_string = retval_string("destination", num_prints, ptr_incrementAmount)
    
    replace_in_file("final_run_again.bt", "final_run_again.bt", "SARGS", source_args_string)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "DARGS", destination_args_string)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "SRETVAL", source_retval_string)
    replace_in_file("final_run_again.bt", "final_run_again.bt", "DRETVAL", destination_retval_string)

