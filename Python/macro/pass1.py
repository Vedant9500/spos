import os

class MNT:
    def __init__(self, name, mdt_index, ala_index):
        self.name = name
        self.mdt_index = mdt_index
        self.ala_index = ala_index

class MacroProcessor:
    mnt = []
    mdt = []
    ala = []

    @staticmethod
    def process(file_path="input.txt"):
        is_macro = False
        mdt_index = 0
        current_ala = -1

        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                if not parts:
                    continue

                if parts[0] == "MACRO":
                    is_macro = True
                    continue

                if is_macro:
                    if parts[0] == "MEND":
                        MacroProcessor.mdt.append("MEND")
                        mdt_index += 1
                        is_macro = False
                        continue

                    if parts[0] == "INCR":
                        MacroProcessor.mdt.append(line.strip())
                        MacroProcessor.mdt.append(f"MOVER AREG, {parts[1].replace('&','')}")
                        MacroProcessor.mdt.append(f"ADD AREG, {parts[2].replace('&','')}")
                        mdt_index += 3

                        arguments = [part for part in parts if '&' in part]
                        MacroProcessor.ala.append(arguments)
                        MacroProcessor.mnt.append(MNT("INCR", mdt_index - 3, current_ala + 1))
                        current_ala += 1

                    elif parts[0] == "DECR":
                        MacroProcessor.mdt.append(line.strip())
                        MacroProcessor.mdt.append(f"MOVER AREG, {parts[1].replace('&','')}")
                        MacroProcessor.mdt.append(f"SUB AREG, {parts[2].replace('&','')}")
                        mdt_index += 3

                        arguments = [part for part in parts if '&' in part]
                        MacroProcessor.ala.append(arguments)
                        MacroProcessor.mnt.append(MNT("DECR", mdt_index - 3, current_ala + 1))
                        current_ala += 1

        MacroProcessor.display_tables()

    @staticmethod
    def display_tables():
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Write MNT
        with open(os.path.join(output_dir, "MNT.txt"), "w") as f:
            f.write("Macro Name Table (MNT):\n")
            f.write("Name\tMDT Index\tALA Index\n")
            for entry in MacroProcessor.mnt:
                f.write(f"{entry.name}\t{entry.mdt_index}\t\t{entry.ala_index}\n")

        # Write MDT
        with open(os.path.join(output_dir, "MDT.txt"), "w") as f:
            f.write("Macro Definition Table (MDT):\n")
            f.write("Index\tDefinition\n")
            for i, entry in enumerate(MacroProcessor.mdt):
                f.write(f"{i}\t{entry}\n")

        # Write ALA
        with open(os.path.join(output_dir, "ALA.txt"), "w") as f:
            f.write("Argument List Array (ALA):\n")
            f.write("Index\tArguments\n")
            for i, args in enumerate(MacroProcessor.ala):
                f.write(f"{i}\t{args}\n")

        print("✅ Output files have been created in the 'output' folder")

# ---------- MAIN ----------
if __name__ == "__main__":
    MacroProcessor.process("input.txt")
