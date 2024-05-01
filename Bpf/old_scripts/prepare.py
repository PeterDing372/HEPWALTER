import subprocess
import json

#container_name = "socialNetwork_social-graph-mongodb.1.jtqfoz0tf6gwdj4lb13s372qb"
container_name = "socialNetwork_social-graph-mongodb.1.zj19mmtvh24e5nvd940h1zq4i"

binary = "/usr/bin/mongod"
# source unmangled name
Source = "mongo::CollectionImpl::isCommitted()"
# dest unmangled name
Dest = "mongo::CollectionCatalog::lookupCollectionByNamespace(mongo::OperationCon"
bufflength = 20

mangledfilename = "manglednames.txt"
unmangledfilename = "unmangledmanglednames.txt"

def get_container_pid(container_name):
    try:
        # Run the docker inspect command and capture the output
        output = subprocess.check_output(['sudo', 'docker', 'inspect', '-f', '{{.State.Pid}}', container_name])
        # Convert the output to string and parse it as JSON
        pid = int(output.decode().strip())
        print("The pid is: ", pid)
        return pid
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


pid = get_container_pid(container_name)

print(f"container name is {container_name} and PID is {pid}")


def find_mangled_name(objdump_T_output, objdump_CT_output, unmangled_name):
    mangled_name = None

    # Parse objdump -CT output to find addresses
    address = ""
    for line in objdump_CT_output.split('\n'):
        if unmangled_name in line:
            print(line)
            address = line.split(' ')[0]
            break

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
        # print(f"There were {len(candidate_mangled_names)} candidate functions: {candidate_mangled_names}")
        # print(f"returning {min(candidate_mangled_names, key=len)}")
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




if __name__ == "__main__":
    with open(mangledfilename, "r") as f:
        objdump_T_output = f.read()

    with open(unmangledfilename, "r") as f:
        objdump_CT_output = f.read()

    mangled_source_name = find_mangled_name(objdump_T_output, objdump_CT_output, Source)
    mangled_dest_name = find_mangled_name(objdump_T_output, objdump_CT_output, Dest)
    replace_in_file("final_template.bt", "final_run.bt", "SOURCE", mangled_source_name)
    replace_in_file("final_run.bt", "final_run.bt", "DEST", mangled_dest_name)
    replace_in_file("final_run.bt", "final_run.bt", "binary", binary)
    replace_in_file("final_run.bt", "final_run.bt", "PID", str(pid))
    replace_in_file("final_run.bt", "final_run.bt","BUFFLENGTH", str(bufflength))
    
