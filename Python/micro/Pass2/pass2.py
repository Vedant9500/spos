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

class Pass2Assembler:
    def __init__(self):
        self.symtab = {}
        self.littab = {}

    def main(self, args=None):
        args = args or []
        cwd = os.getcwd() + os.sep

        intermediate_file = args[0] if len(args) >= 1 else cwd + "intermediate_code.txt"
        sym_file = args[1] if len(args) >= 2 else cwd + "symbol_table.txt"
        lit_file = args[2] if len(args) >= 3 else cwd + "literal_table.txt"
        pool_file = args[3] if len(args) >= 4 else cwd + "pool_table.txt"
        output_file = args[4] if len(args) >= 5 else cwd + "Machinecode.txt"

        # ✅ Check if files exist
        for fpath, label in [
            (sym_file, "Symbol table"),
            (lit_file, "Literal table"),
            (intermediate_file, "Intermediate code"),
            (pool_file, "Pool table")
        ]:
            if not os.path.exists(fpath):
                print(f"❌ Error: {label} file not found: {fpath}")
                return

        print("Reading input files...")

        try:
            self.load_symtab(sym_file)
            self.load_littab(lit_file)
            self.generate_machine_code(intermediate_file, output_file)
            print(f"✅ Machine code generated successfully: {output_file}")
        except Exception as e:
            print(f"❌ Error processing files: {e}")

    # ---------- LOAD SYMBOL TABLE ----------
    def load_symtab(self, file):
        print(f"Loading symbol table from: {file}")
        with open(file, "r") as f:
            header_skipped = False
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not header_skipped:
                    header_skipped = True
                    continue
                parts = re.split(r"\s+", line)
                if len(parts) >= 3:
                    try:
                        index = int(parts[0])
                        name = parts[1]
                        addr = int(parts[2])
                        self.symtab[index] = Symbol(name, addr)
                    except ValueError:
                        continue

    # ---------- LOAD LITERAL TABLE ----------
    def load_littab(self, file):
        print(f"Loading literal table from: {file}")
        with open(file, "r") as f:
            header_skipped = False
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if not header_skipped:
                    header_skipped = True
                    continue
                parts = re.split(r"\s+", line)
                if len(parts) >= 3:
                    try:
                        index = int(parts[0])
                        literal = parts[1]
                        addr = int(parts[2])
                        self.littab[index] = Literal(literal, addr)
                    except ValueError:
                        continue

    # ---------- GENERATE MACHINE CODE ----------
    def generate_machine_code(self, file, output_file):
        with open(output_file, "w") as out:
            out.write("Address\tMachine Code\n")
            out.write("------------------------\n")

            with open(file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split()
                    addr = parts[0].replace(":", "")
                    machine = ""

                    # Skip Assembler Directives
                    if "(AD," in line:
                        continue

                    # ---- IS (Imperative Statements) ----
                    if "(IS," in line:
                        match = re.search(r"\(IS,(\d+)\)", line)
                        if match:
                            opcode = match.group(1)
                            machine += opcode + " "

                            reg_match = re.search(r"\(RG,(\d+)\)", line)
                            reg_code = reg_match.group(1) if reg_match else "0"
                            machine += reg_code + " "

                            if "(S," in line:
                                sym_match = re.search(r"\(S,(\d+)\)", line)
                                if sym_match:
                                    sym_index = int(sym_match.group(1))
                                    sym = self.symtab.get(sym_index)
                                    machine += str(sym.address if sym else 0)
                            elif "(L," in line:
                                lit_match = re.search(r"\(L,(\d+)\)", line)
                                if lit_match:
                                    lit_index = int(lit_match.group(1))
                                    lit = self.littab.get(lit_index)
                                    machine += str(lit.address if lit else 0)

                    # ---- DL (Declarative Statements) ----
                    elif "(DL," in line:
                        c_match = re.search(r"\(C,(\d+)\)", line)
                        if c_match:
                            const_val = c_match.group(1)
                            machine += f"00 0 {const_val}"
                        else:
                            machine += "00 0 0"

                    if machine:
                        out.write(f"{addr}\t{machine.strip()}\n")

# ---------- MAIN ----------
if __name__ == "__main__":
    assembler = Pass2Assembler()
    assembler.main()
