# Macro Definition Table (MDT)
MDT = [
    "INCR &ARG1, &ARG2",
    "MOVER AREG, &ARG1",
    "ADD AREG, &ARG2",
    "MEND",
    "DECR &ARG3, &ARG4",
    "MOVER AREG, &ARG3",
    "SUB AREG, &ARG4",
    "MEND"
]

# Macro Name Table (MNT) -> Macro Name : Index in MDT
MNT = {
    "INCR": 0,
    "DECR": 4
}

# Argument List Array (ALA) -> Macro Name : List of formal parameters
ALA = {
    "INCR": ["&ARG1", "&ARG2"],
    "DECR": ["&ARG3", "&ARG4"]
}

# Intermediate code with macro calls
intermediate_code = [
    "START",
    "INCR N1, N2",
    "DECR N3, N4",
    "END"
]

# Function to expand a macro call
def expand_macro(macro_name, actual_args):
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

# Pass-II: Expand macros in intermediate code
output_code = []

for line in intermediate_code:
    parts = line.split()
    if parts[0] in MNT:
        macro_name = parts[0]
        args = parts[1].split(",")
        expanded_lines = expand_macro(macro_name, args)
        output_code.extend(expanded_lines)
    else:
        output_code.append(line)

# Print the output
print("Output Code after Pass-II Macro Expansion:")
for line in output_code:
    print(line)
