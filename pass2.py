import os
import re

class Symbol:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Literal:
    def __init__(self, literal, address):
        self.literal = literal
        self.address = address


symtab = {}
littab = {}


def load_symtab(file_path):
    print(f"Loading symbol table from: {file_path}")
    with open(file_path, "r") as f:
        lines = f.readlines()

    header_skipped = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not header_skipped:
            header_skipped = True
            continue  # Skip header line

        parts = line.split()
        if len(parts) >= 3:
            try:
                index = int(parts[0])
                name = parts[1]
                addr = int(parts[2])
                symtab[index] = Symbol(name, addr)
            except ValueError:
                continue  # Skip invalid lines silently


def load_littab(file_path):
    print(f"Loading literal table from: {file_path}")
    with open(file_path, "r") as f:
        lines = f.readlines()

    header_skipped = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not header_skipped:
            header_skipped = True
            continue  # Skip header line

        parts = line.split()
        if len(parts) >= 3:
            try:
                index = int(parts[0])
                literal = parts[1]
                addr = int(parts[2])
                littab[index] = Literal(literal, addr)
            except ValueError:
                continue


def generate_machine_code(intermediate_file, output_file):
    with open(output_file, "w") as bw:
        bw.write("Address\tMachine Code\n")
        bw.write("------------------------\n")

        with open(intermediate_file, "r") as br:
            for line in br:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                addr = parts[0].replace(":", "")
                machine = ""

                # Skip AD (Assembler Directive)
                if "(AD," in line:
                    continue

                # Handle IS (Imperative Statement)
                if "(IS," in line:
                    match = re.search(r"\(IS,(\d+)\)", line)
                    if match:
                        machine += match.group(1) + " "

                        # Register
                        reg_match = re.search(r"\(RG,(\d+)\)", line)
                        if reg_match:
                            machine += reg_match.group(1) + " "
                        else:
                            machine += "0 "

                        # Symbol operand
                        sym_match = re.search(r"\(S,(\d+)\)", line)
                        if sym_match:
                            sym_index = int(sym_match.group(1))
                            sym = symtab.get(sym_index)
                            machine += str(sym.address if sym else 0)

                        # Literal operand
                        lit_match = re.search(r"\(L,(\d+)\)", line)
                        if lit_match:
                            lit_index = int(lit_match.group(1))
                            lit = littab.get(lit_index)
                            machine += str(lit.address if lit else 0)

                # Handle DL (Declarative)
                elif "(DL," in line:
                    const_match = re.search(r"\(C,(\d+)\)", line)
                    if const_match:
                        machine += f"00 0 {const_match.group(1)}"
                    else:
                        machine += "00 0 0"

                if machine:
                    bw.write(f"{addr}\t{machine.strip()}\n")


def main():
    # ✅ Use current directory as default base path
    base_dir = os.getcwd() + os.sep

    intermediate_file = os.path.join(base_dir, "intermediate_code.txt")
    sym_file = os.path.join(base_dir, "symbol_table.txt")
    lit_file = os.path.join(base_dir, "literal_table.txt")
    pool_file = os.path.join(base_dir, "pool_table.txt")
    output_file = os.path.join(base_dir, "Machinecode.txt")

    # File existence check
    for file in [sym_file, lit_file, intermediate_file, pool_file]:
        if not os.path.exists(file):
            print(f"Error: File not found -> {file}")
            return

    print("Reading input files...")

    try:
        load_symtab(sym_file)
        load_littab(lit_file)
        generate_machine_code(intermediate_file, output_file)
        print(f"✅ Machine code generated successfully in {output_file}")
    except Exception as e:
        print(f"Error processing files: {e}")


if __name__ == "__main__":
    main()
