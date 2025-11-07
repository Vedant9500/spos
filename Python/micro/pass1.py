import re

class Symbol:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Literal:
    def __init__(self, value, address):
        self.value = value
        self.address = address

class PassOne:
    MOT = {
        "STOP": 0, "ADD": 1, "SUB": 2, "MULT": 3,
        "MOVER": 4, "MOVEM": 5, "BC": 6,
        "LTORG": -1, "START": -2, "END": -3,
        "ORIGIN": -4, "EQU": -5, "DS": -6
    }

    REG = {"AREG": 1, "BREG": 2, "CREG": 3}

    def __init__(self):
        self.SYMTAB = []
        self.LITTAB = []
        self.POOLTAB = []
        self.IC = []
        self.LC = 0
        self.lastLitIndex = 0

    # ---------- Core Processing ----------
    def process(self, filename="input.txt"):
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = re.split(r"[ ,]+", line)
                label, op, op1, op2 = "", "", "", ""
                idx = 0

                if parts[0] not in self.MOT:
                    label = parts[0]
                    idx = 1
                if idx < len(parts): op = parts[idx]; idx += 1
                if idx < len(parts): op1 = parts[idx]; idx += 1
                if idx < len(parts): op2 = parts[idx]

                if label:
                    if op != "EQU":
                        self.add_or_update_symbol(label, self.LC)
                    else:
                        self.add_or_update_symbol(label, -1)

                if op == "START":
                    self.LC = int(op1) if op1 else 0
                    self.add_ic(self.LC, f"(AD,START) (C,{self.LC})")

                elif op == "ORIGIN":
                    self.LC = self.evaluate(op1)
                    self.add_ic(self.LC, f"(AD,ORIGIN) (C,{self.LC})")

                elif op == "EQU":
                    addr = self.evaluate(op1)
                    sym_index = self.get_sym_index(label)
                    self.SYMTAB[sym_index].address = addr
                    self.add_ic(self.LC, f"(AD,EQU) (S,{sym_index+1}) (C,{addr})")

                elif op in ("LTORG", "END"):
                    if self.lastLitIndex < len(self.LITTAB):
                        self.POOLTAB.append(self.lastLitIndex + 1)
                        self.add_ic(self.LC, "(AD,LTORG)")
                        for i in range(self.lastLitIndex, len(self.LITTAB)):
                            lit = self.LITTAB[i]
                            lit.address = self.LC
                            self.add_ic(self.LC, f"(DL,01) (C,{self.literal_value_number(lit.value)})")
                            self.LC += 1
                        self.lastLitIndex = len(self.LITTAB)
                    else:
                        self.add_ic(self.LC, "(AD,LTORG)")

                    if op == "END":
                        self.add_ic(self.LC, "(AD,END)")

                elif op == "DS":
                    si = self.get_sym_index(label)
                    self.SYMTAB[si].address = self.LC
                    self.add_ic(self.LC, f"(DL,DS) (C,{op1})")
                    self.LC += int(op1)

                else:
                    # Normal Instruction
                    if op in self.MOT and self.MOT[op] >= 0:
                        mot_code = self.MOT[op]
                        reg_code = "0"
                        if op1 and op1 in self.REG:
                            reg_code = str(self.REG[op1])

                        if op2 and self.is_literal(op2):
                            self.LITTAB.append(Literal(op2, -1))
                            lit_index = len(self.LITTAB)
                            self.add_ic(self.LC, f"(IS,{mot_code:02d}) (RG,{reg_code}) (L,{lit_index})")
                        elif op2:
                            sym_idx = self.get_sym_index(op2)
                            self.add_ic(self.LC, f"(IS,{mot_code:02d}) (RG,{reg_code}) (S,{sym_idx+1})")
                        else:
                            self.add_ic(self.LC, f"(IS,{mot_code:02d}) (RG,{reg_code})")

                        self.LC += 1

        # Output all results
        self.print_tables()
        self.write_symbol_table("symbol_table.txt")
        self.write_literal_table("literal_table.txt")
        self.write_pool_table("pool_table.txt")
        self.write_intermediate_file("intermediate_code.txt")

        print("\nFiles written: symbol_table.txt, literal_table.txt, pool_table.txt, intermediate_code.txt")

    # ---------- Helper Methods ----------
    def is_literal(self, op):
        return op.startswith("=")

    def literal_value_number(self, lit):
        if not lit:
            return 0
        val = lit.strip().lstrip("=").strip("'\"")
        return int(val) if val.isdigit() else 0

    def add_or_update_symbol(self, sym, addr):
        for s in self.SYMTAB:
            if s.name == sym:
                if addr >= 0:
                    s.address = addr
                return
        self.SYMTAB.append(Symbol(sym, addr))

    def get_sym_index(self, sym):
        for i, s in enumerate(self.SYMTAB):
            if s.name == sym:
                return i
        self.SYMTAB.append(Symbol(sym, -1))
        return len(self.SYMTAB) - 1

    def get_symbol_addr(self, sym):
        for s in self.SYMTAB:
            if s.name == sym:
                return s.address
        return -1

    def evaluate(self, expr):
        expr = expr.strip()
        if expr.isdigit():
            return int(expr)
        if "+" in expr:
            base, off = expr.split("+")
            return (self.get_symbol_addr(base) or 0) + int(off)
        if "-" in expr:
            base, off = expr.split("-")
            return (self.get_symbol_addr(base) or 0) - int(off)
        return self.get_symbol_addr(expr) or 0

    def add_ic(self, lc, code):
        self.IC.append(f"{lc} : {code}")

    # ---------- Printing and File Writing ----------
    def print_tables(self):
        print("\n--- SYMBOL TABLE ---")
        for i, s in enumerate(self.SYMTAB, start=1):
            print(f"{i}\t{s.name}\t{s.address}")

        print("\n--- LITERAL TABLE ---")
        for i, l in enumerate(self.LITTAB, start=1):
            print(f"{i}\t{l.value}\t{l.address}")

        print("\n--- POOL TABLE ---")
        for i, p in enumerate(self.POOLTAB, start=1):
            print(f"#{i}\t{p}")

        print("\n--- INTERMEDIATE CODE ---")
        for s in self.IC:
            print(s)

    def write_symbol_table(self, fname):
        with open(fname, "w") as f:
            f.write("Index\tSymbol\tAddress\n")
            for i, s in enumerate(self.SYMTAB, start=1):
                f.write(f"{i}\t{s.name}\t{s.address}\n")

    def write_literal_table(self, fname):
        with open(fname, "w") as f:
            f.write("Index\tLiteral\tAddress\n")
            for i, l in enumerate(self.LITTAB, start=1):
                f.write(f"{i}\t{l.value}\t{l.address}\n")

    def write_pool_table(self, fname):
        with open(fname, "w") as f:
            f.write("PoolIndex\tStartLiteralIndex\n")
            for i, p in enumerate(self.POOLTAB, start=1):
                f.write(f"#{i}\t{p}\n")

    def write_intermediate_file(self, fname):
        with open(fname, "w") as f:
            for s in self.IC:
                f.write(s + "\n")

# ---------- Run the Program ----------
if __name__ == "__main__":
    assembler = PassOne()
    assembler.process("input.txt")
