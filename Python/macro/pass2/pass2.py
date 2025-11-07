# Function to read MDT from file
def read_mdt(file_name):
    with open(file_name, "r") as f:
        return [line.strip() for line in f.readlines()]

# Function to read MNT from file
def read_mnt(file_name):
    mnt = {}
    with open(file_name, "r") as f:
        for line in f:
            parts = line.strip().split()
            mnt[parts[0]] = int(parts[1])
    return mnt

# Function to read ALA from file
def read_ala(file_name):
    ala = {}
    with open(file_name, "r") as f:
        for line in f:
            parts = line.strip().split()
            macro_name = parts[0]
            args = parts[1].split(",")
            ala[macro_name] = args
    return ala

# Function to read intermediate code
def read_intermediate(file_name):
    with open(file_name, "r") as f:
        return [line.strip() for line in f.readlines()]

# Function to expand a macro call
def expand_macro(macro_name, actual_args, MDT, MNT, ALA):
    start_index = MNT[macro_name]
    formal_args = ALA[macro_name]
    expanded_code = []

    i = start_index + 1  # skip the macro header
    while MDT[i] != "MEND":
        line = MDT[i]
        for j in range(len(formal_args)):
            line = line.replace(formal_args[j], actual_args[j])
        expanded_code.append(line)
        i += 1

    return expanded_code

# Main function
def pass2_macroprocessor():
    MDT = read_mdt("MDT.txt")
    MNT = read_mnt("MNT.txt")
    ALA = read_ala("ALA.txt")
    intermediate_code = read_intermediate("intermediate.txt")

    output_code = []

    for line in intermediate_code:
        parts = line.split()
        if parts[0] in MNT:
            macro_name = parts[0]
            args = parts[1].split(",")
            expanded_lines = expand_macro(macro_name, args, MDT, MNT, ALA)
            output_code.extend(expanded_lines)
        else:
            output_code.append(line)

    # Write output to a text file
    with open("output.txt", "w") as f:
        for line in output_code:
            f.write(line + "\n")

    print("Macro expansion complete. Output written to output.txt")

# Run the macroprocessor
pass2_macroprocessor()
