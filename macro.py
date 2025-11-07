import os
from collections import OrderedDict


class MacroEntry:
    def __init__(self, mdt_index, params, defaults):
        self.mdt_index = mdt_index
        self.params = params
        self.defaults = defaults


class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class MacroProcessor:
    def __init__(self):
        self.MNT = OrderedDict()          # Macro Name Table
        self.MDT = []                     # Macro Definition Table
        self.intermediate_code = []       # Intermediate Code (Non-macro lines)

    # ---------- Parse Macro Header ----------
    def parse_macro_header(self, line, mdt_index):
        parts = line.strip().split()
        macro_name = parts[0]

        params = []
        defaults = OrderedDict()

        if len(parts) > 1:
            param_str = line[len(macro_name):].replace(" ", "")
            param_list = param_str.split(",")

            for p in param_list:
                if "=" in p:
                    kv = p.split("=")
                    param_name = kv[0]
                    default_val = kv[1] if len(kv) > 1 and kv[1] else None
                    params.append(param_name)
                    defaults[param_name] = default_val
                else:
                    params.append(p)

        return MacroEntry(mdt_index, params, defaults)

    # ---------- Pass 1 ----------
    def pass1(self, source_lines):
        in_macro = False
        current_macro = None
        param_list = []
        default_params = OrderedDict()
        mdt_index = 0

        for raw_line in source_lines:
            line = raw_line.strip()
            if not line:
                continue

            if line == "MACRO":
                in_macro = True
                continue

            if in_macro:
                if current_macro is None:
                    # Parse header
                    entry = self.parse_macro_header(line, mdt_index)
                    current_macro = line.split()[0]
                    param_list = entry.params
                    default_params = entry.defaults
                    self.MNT[current_macro] = entry
                else:
                    processed_line = line
                    for i, param in enumerate(param_list):
                        processed_line = processed_line.replace(param, f"(P,{i})")
                    self.MDT.append(processed_line)
                    mdt_index += 1

                    if processed_line == "MEND":
                        in_macro = False
                        current_macro = None
                        param_list.clear()
                        default_params.clear()
            else:
                self.intermediate_code.append(line)

    # ---------- Pass 2 ----------
    def pass2(self):
        output = []
        all_alas = []

        for line in self.intermediate_code:
            parts = line.strip().split()
            if not parts:
                output.append(line)
                continue

            macro_name = parts[0]
            if macro_name in self.MNT:
                entry = self.MNT[macro_name]
                formal_params = entry.params
                defaults = entry.defaults

                actual_params_str = line[len(macro_name):].strip()
                ALA = OrderedDict()

                # Actual parameters
                if actual_params_str:
                    tokens = actual_params_str.split(",")
                    pos_index = 0
                    for tok in tokens:
                        tok = tok.strip()
                        if "=" in tok:
                            kv = tok.split("=")
                            key = kv[0].strip()
                            val = kv[1].strip()
                            if not key.startswith("&"):
                                key = "&" + key
                            ALA[key] = val
                        else:
                            if pos_index < len(formal_params):
                                ALA[formal_params[pos_index]] = tok
                                pos_index += 1

                # Fill defaults
                for p in formal_params:
                    if p not in ALA:
                        ALA[p] = defaults.get(p, "")

                all_alas.append({macro_name: dict(ALA)})

                # Expand macro
                i = entry.mdt_index
                while i < len(self.MDT):
                    mdt_line = self.MDT[i]
                    if mdt_line == "MEND":
                        break

                    expanded_line = mdt_line
                    for idx, formal in enumerate(formal_params):
                        expanded_line = expanded_line.replace(f"(P,{idx})", ALA.get(formal, ""))
                    output.append(expanded_line)
                    i += 1
            else:
                output.append(line)

        return Pair(output, all_alas)

    # ---------- File Writer ----------
    def write_to_file(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)

    # ---------- Generate Output Files ----------
    def generate_files(self, expanded_code, all_alas):
        # MNT
        mnt_content = ["=== MNT (Macro Name Table) ==="]
        for name, entry in self.MNT.items():
            mnt_content.append(f"{name}:")
            mnt_content.append(f"  MDT index: {entry.mdt_index}")
            mnt_content.append(f"  Params: {entry.params}")
            mnt_content.append(f"  Defaults: {entry.defaults}")
        self.write_to_file("mnt.txt", "\n".join(mnt_content))

        # MDT
        mdt_content = ["=== MDT (Macro Definition Table) ==="]
        for i, line in enumerate(self.MDT):
            mdt_content.append(f"{i}: {line}")
        self.write_to_file("mdt.txt", "\n".join(mdt_content))

        # Intermediate Code
        ic_content = ["=== Intermediate Code (Pass-I Output) ==="]
        ic_content.extend(self.intermediate_code)
        self.write_to_file("intermediate_code.txt", "\n".join(ic_content))

        # ALAs
        ala_content = ["=== ALAs for each Macro Invocation ==="]
        for idx, ala in enumerate(all_alas, start=1):
            ala_content.append(f"Invocation {idx}: {ala}")
        self.write_to_file("alas.txt", "\n".join(ala_content))

        # Expanded Code
        exp_content = ["=== Expanded Code (Pass-II Output) ==="]
        exp_content.extend(expanded_code)
        self.write_to_file("expanded_code.txt", "\n".join(exp_content))


# ---------- Main ----------
if __name__ == "__main__":
    source_program = [
        "MACRO",
        "INCR_D  &MEM_VAL, &INCR_VAL=, &REG=AREG",
        "MOVER &REG, &MEM_VAL",
        "ADD &REG, &INCR_VAL",
        "MOVEM &REG, &MEM_VAL",
        "MEND",
        "START 200",
        "DS A 1",
        "DC B 1",
        "INCR_D A, INCR_VAL=B, REG=BREG",
        "INCR_D A, INCR_VAL=B",
        "PRINT A",
        "END 202"
    ]

    mp = MacroProcessor()
    mp.pass1(source_program)

    result = mp.pass2()
    expanded_code = result.first
    all_alas = result.second

    mp.generate_files(expanded_code, all_alas)
    print("✅ Macro processing completed. Files generated:")
    print(" - mnt.txt")
    print(" - mdt.txt")
    print(" - intermediate_code.txt")
    print(" - alas.txt")
    print(" - expanded_code.txt")
