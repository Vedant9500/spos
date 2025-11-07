import os

class MNT:
    def __init__(self, name, mdt_index, ala_index):
        self.name = name
        self.mdt_index = mdt_index
        self.ala_index = ala_index

class MacroProcessor2:
    mnt = []
    mdt = []

    @staticmethod
    def process(input_file="input.txt"):
        MacroProcessor2.read_tables()

        os.makedirs("output", exist_ok=True)
        expanded_file = os.path.join("output", "expanded_code.txt")

        with open(input_file, "r") as f, open(expanded_file, "w") as out:
            processing_macro = False

            for line in f:
                trimmed = line.strip()
                if not trimmed:
                    continue

                if trimmed == "START" or trimmed == "END":
                    out.write(trimmed + "\n")
                    continue

                if trimmed == "MACRO":
                    processing_macro = True
                    continue

                if processing_macro:
                    if trimmed == "MEND":
                        processing_macro = False
                    continue

                # Parse macro calls
                tokens = trimmed.split()
                if not tokens:
                    continue

                opcode = tokens[0]
                if opcode in ("INCR", "DECR"):
                    args_part = trimmed[len(opcode):].strip()
                    macro_args = [arg.strip() for arg in args_part.split(",") if arg.strip()]

                    # fallback: space-separated args
                    if len(macro_args) < 2 and len(tokens) >= 3:
                        macro_args = [tokens[1].replace(",", ""), tokens[2].replace(",", "")]

                    if len(macro_args) < 2:
                        print(f"⚠️ Invalid macro call (expected 2 args): {line}")
                        continue

                    MacroProcessor2.expand_macro(opcode, macro_args, out)
                else:
                    # Non-macro line: copy as-is
                    out.write(trimmed + "\n")

        print("✅ Macro expansion completed. Check 'output/expanded_code.txt'")

    @staticmethod
    def read_tables():
        # Read MDT
        try:
            with open("output/MDT.txt", "r") as f:
                next(f)  # skip header
                next(f)
                for line in f:
                    if line.strip():
                        parts = line.split("\t")
                        if len(parts) > 1:
                            MacroProcessor2.mdt.append(parts[-1].strip())
                        else:
                            MacroProcessor2.mdt.append(line.strip().split(None, 1)[-1])
        except FileNotFoundError:
            print("⚠️ MDT file not found. Please run pass1 first.")
            return

        # Read MNT
        try:
            with open("output/MNT.txt", "r") as f:
                next(f)
                next(f)
                for line in f:
                    tokens = line.strip().split()
                    if len(tokens) >= 3:
                        try:
                            name = tokens[0].strip()
                            mdt_index = int(tokens[1].strip())
                            ala_index = int(tokens[2].strip())
                            MacroProcessor2.mnt.append(MNT(name, mdt_index, ala_index))
                        except ValueError:
                            print(f"⚠️ Skipping invalid MNT entry: {line}")
                    else:
                        print(f"⚠️ Skipping invalid MNT entry: {line}")
        except FileNotFoundError:
            print("⚠️ MNT file not found. Please run pass1 first.")
            return

    @staticmethod
    def expand_macro(macro_name, args, writer):
        if macro_name == "INCR":
            writer.write(f"MOVER AREG, {args[0].strip()}\n")
            writer.write(f"ADD AREG, {args[1].strip()}\n")
        elif macro_name == "DECR":
            writer.write(f"MOVER AREG, {args[0].strip()}\n")
            writer.write(f"SUB AREG, {args[1].strip()}\n")


# ------------------- MAIN -------------------
if __name__ == "__main__":
    MacroProcessor2.process("input.txt")
