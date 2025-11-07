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
    MOT = {}
    REG = {}
    SYMTAB = []
    LITTAB = []
    POOLTAB = []
    IC = []

    LC = 0
    lastLitIndex = 0

    @staticmethod
    def initialize_tables():
        PassOne.MOT = {
            "STOP": 0, "ADD": 1, "SUB": 2, "MULT": 3,
            "MOVER": 4, "MOVEM": 5, "BC": 6,
            "LTORG": -1, "START": -2, "END": -3,
            "ORIGIN": -4, "EQU": -5, "DS": -6
        }

        PassOne.REG = {"AREG": 1, "BREG": 2, "CREG": 3}

    @staticmethod
    def is_literal(op):
        return op.startswith("=")

    @staticmethod
    def literal_value_number(lit):
        if not lit:
            return 0
        t = lit.strip()
        if t.startswith("="):
            t = t[1:]
        t = re.sub(r"[\'\"]", "", t)
        try:
            return int(t)
        except ValueError:
            return 0

    @staticmethod
    def add_or_update_symbol(sym, addr):
        for s in PassOne.SYMTAB:
            if s.name == sym:
                if addr >= 0:
                    s.address = addr
                return
        PassOne.SYMTAB.append(Symbol(sym, addr))

    @staticmethod
    def get_sym_index(sym):
        for i, s in enumerate(PassOne.SYMTAB):
            if s.name == sym:
                return i
        PassOne.SYMTAB.append(Symbol(sym, -1))
        return len(PassOne.SYMTAB) - 1

    @staticmethod
    def get_symbol_addr(sym):
        for s in PassOne.SYMTAB:
            if s.name == sym:
                return s.address
        return -1

    @staticmethod
    def evaluate(expr):
        expr = expr.strip()
        if re.fullmatch(r"\d+", expr):
            return int(expr)
        if "+" in expr:
            base, off = expr.split("+")
            return max(PassOne.get_symbol_addr(base), 0) + int(off)
        elif "-" in expr:
            base, off = expr.split("-")
            return max(PassOne.get_symbol_addr(base), 0) - int(off)
        else:
            a = PassOne.get_symbol_addr(expr)
            return a if a >= 0 else 0

    @staticmethod
    def add_ic(lc, code):
        PassOne.IC.append(f"{lc} : {code}")

    @staticmethod
    def process():
        with open("input.txt", "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = re.split(r"[ ,]+", line)
                label, op, op1, op2 = "", "", "", ""
                idx = 0

                if parts[0] not in PassOne.MOT:
                    label = parts[0]
                    idx = 1
                if idx < len(parts):
                    op = parts[idx]
                    idx += 1
                if idx < len(parts):
                    op1 = parts[idx]
                    idx += 1
                if idx < len(parts):
                    op2 = parts[idx]

                # Handle label
                if label:
                    if op != "EQU":
                        PassOne.add_or_update_symbol(label, PassOne.LC)
                    else:
                        PassOne.add_or_update_symbol(label, -1)

                # Process operations
                if op == "START":
                    PassOne.LC = int(op1) if op1 else 0
                    PassOne.add_ic(PassOne.LC, f"(AD,START) (C,{PassOne.LC})")

                elif op == "ORIGIN":
                    PassOne.LC = PassOne.evaluate(op1)
                    PassOne.add_ic(PassOne.LC, f"(AD,ORIGIN) (C,{PassOne.LC})")

                elif op == "EQU":
                    addr = PassOne.evaluate(op1)
                    si = PassOne.get_sym_index(label)
                    PassOne.SYMTAB[si].address = addr
                    PassOne.add_ic(PassOne.LC, f"(AD,EQU) (S,{si+1}) (C,{addr})")

                elif op in ("LTORG", "END"):
                    if PassOne.lastLitIndex < len(PassOne.LITTAB):
                        PassOne.POOLTAB.append(PassOne.lastLitIndex + 1)
                        PassOne.add_ic(PassOne.LC, "(AD,LTORG)")
                        for i in range(PassOne.lastLitIndex, len(PassOne.LITTAB)):
                            PassOne.LITTAB[i].address = PassOne.LC
                            val = PassOne.literal_value_number(PassOne.LITTAB[i].value)
                            PassOne.add_ic(PassOne.LC, f"(DL,01) (C,{val})")
                            PassOne.LC += 1
                        PassOne.lastLitIndex = len(PassOne.LITTAB)
                    else:
                        PassOne.add_ic(PassOne.LC, "(AD,LTORG)")

                    if op == "END":
                        PassOne.add_ic(PassOne.LC, "(AD,END)")

                elif op == "DS":
                    si = PassOne.get_sym_index(label)
                    PassOne.SYMTAB[si].address = PassOne.LC
                    PassOne.add_ic(PassOne.LC, f"(DL,DS) (C,{op1})")
                    PassOne.LC += int(op1)

                else:
                    if op in PassOne.MOT and PassOne.MOT[op] >= 0:
                        mot_code = PassOne.MOT[op]
                        reg_code = "0"
                        if op1 and op1 in PassOne.REG:
                            reg_code = str(PassOne.REG[op1])
                        if op2 and PassOne.is_literal(op2):
                            PassOne.LITTAB.append(Literal(op2, -1))
                            lit_idx = len(PassOne.LITTAB)
                            PassOne.add_ic(PassOne.LC, f"(IS,{mot_code:02d}) (RG,{reg_code}) (L,{lit_idx})")
                        elif op2:
                            sym_idx = PassOne.get_sym_index(op2)
                            PassOne.add_ic(PassOne.LC, f"(IS,{mot_code:02d}) (RG,{reg_code}) (S,{sym_idx+1})")
                        else:
                            PassOne.add_ic(PassOne.LC, f"(IS,{mot_code:02d}) (RG,{reg_code})")
                        PassOne.LC += 1

    @staticmethod
    def print_tables():
        print("\n--- SYMBOL TABLE ---")
        for i, s in enumerate(PassOne.SYMTAB, start=1):
            print(f"{i}\t{s.name}\t{s.address}")

        print("\n--- LITERAL TABLE ---")
        for i, l in enumerate(PassOne.LITTAB, start=1):
            print(f"{i}\t{l.value}\t{l.address}")

        print("\n--- POOL TABLE ---")
        for i, p in enumerate(PassOne.POOLTAB, start=1):
            print(f"#{i}\t{p}")

        print("\n--- INTERMEDIATE CODE ---")
        for s in PassOne.IC:
            print(s)

    @staticmethod
    def write_to_file():
        with open("symbol_table.txt", "w") as f:
            f.write("Index\tSymbol\tAddress\n")
            for i, s in enumerate(PassOne.SYMTAB, start=1):
                f.write(f"{i}\t{s.name}\t{s.address}\n")

        with open("literal_table.txt", "w") as f:
            f.write("Index\tLiteral\tAddress\n")
            for i, l in enumerate(PassOne.LITTAB, start=1):
                f.write(f"{i}\t{l.value}\t{l.address}\n")

        with open("pool_table.txt", "w") as f:
            f.write("PoolIndex\tStartLiteralIndex\n")
            for i, p in enumerate(PassOne.POOLTAB, start=1):
                f.write(f"#{i}\t{p}\n")

        with open("intermediate_code.txt", "w") as f:
            for s in PassOne.IC:
                f.write(s + "\n")

# Run assembler
if __name__ == "__main__":
    PassOne.initialize_tables()
    PassOne.process()
    PassOne.print_tables()
    PassOne.write_to_file()
    print("\nFiles written: symbol_table.txt, literal_table.txt, pool_table.txt, intermediate_code.txt")
