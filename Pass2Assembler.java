import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Pass2Assembler {

    static class Symbol {
        String name;
        int address;
        Symbol(String n, int a) { name = n; address = a; }
    }

    static class Literal {
        String literal;
        int address;
        Literal(String l, int a) { literal = l; address = a; }
    }

    static Map<Integer, Symbol> symtab = new HashMap<>();
    static Map<Integer, Literal> littab = new HashMap<>();

    public static void main(String[] args) throws Exception {
        String baseDir = "c:\\Users\\DNYANESHWAR\\OneDrive\\Desktop\\finalspos\\";
        String intermediateFile = baseDir + "intermediate_code.txt";  // Changed from intermediate.txt
        String symFile = baseDir + "symbol_table.txt";
        String litFile = baseDir + "literal_table.txt";
        String poolFile = baseDir + "pool_table.txt";    // Added pool table file
        String outputFile = baseDir + "Machinecode.txt";

        // Check if input files exist
        File symFileObj = new File(symFile);
        File litFileObj = new File(litFile);
        File intFileObj = new File(intermediateFile);
        File poolFileObj = new File(poolFile);           // Added pool file check

        if (!symFileObj.exists()) {
            System.err.println("Error: Symbol table file not found: " + symFile);
            return;
        }
        if (!litFileObj.exists()) {
            System.err.println("Error: Literal table file not found: " + litFile);
            return;
        }
        if (!intFileObj.exists()) {
            System.err.println("Error: Intermediate file not found: " + intermediateFile);
            return;
        }
        if (!poolFileObj.exists()) {
            System.err.println("Error: Pool table file not found: " + poolFile);
            return;
        }

        System.out.println("Reading input files...");
        try {
            loadSymtab(symFile);
            loadLittab(litFile);
            generateMachineCode(intermediateFile, outputFile);
            System.out.println("Machine code generated successfully in " + outputFile);
        } catch (IOException e) {
            System.err.println("Error processing files: " + e.getMessage());
            e.printStackTrace();
        }
    }

    static void loadSymtab(String file) throws IOException {
        System.out.println("Loading symbol table from: " + file);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            boolean headerSkipped = false;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) continue;
                if (!headerSkipped) {
                    headerSkipped = true;
                    continue;  // Skip the header line
                }
                String[] parts = line.split("\\s+");
                if (parts.length >= 3) {
                    try {
                        int index = Integer.parseInt(parts[0]);
                        String name = parts[1];
                        int addr = Integer.parseInt(parts[2]);
                        symtab.put(index, new Symbol(name, addr));
                    } catch (NumberFormatException e) {
                        // Skip invalid lines silently
                    }
                }
            }
        }
    }

    static void loadLittab(String file) throws IOException {
        System.out.println("Loading literal table from: " + file);
        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;
            boolean headerSkipped = false;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) continue;
                if (!headerSkipped) {
                    headerSkipped = true;
                    continue;  // Skip the header line
                }
                String[] parts = line.split("\\s+");
                if (parts.length >= 3) {
                    try {
                        int index = Integer.parseInt(parts[0]);
                        String literal = parts[1];
                        int addr = Integer.parseInt(parts[2]);
                        littab.put(index, new Literal(literal, addr));
                    } catch (NumberFormatException e) {
                        // Skip invalid lines silently
                    }
                }
            }
        }
    }

    static void generateMachineCode(String file, String outputFile) throws IOException {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile))) {
            bw.write("Address\tMachine Code\n");
            bw.write("------------------------\n");

            try (BufferedReader br = new BufferedReader(new FileReader(file))) {
                String line;
                while ((line = br.readLine()) != null) {
                    line = line.trim();
                    if (line.isEmpty()) continue;

                    String[] parts = line.split("\\s+");
                    String addr = parts[0].replace(":", "");
                    StringBuilder machine = new StringBuilder();

                    // Skip AD instructions
                    if (line.contains("(AD,")) continue;

                    // Handle IS instructions
                    if (line.contains("(IS,")) {
                        Pattern p = Pattern.compile("\\(IS,(\\d+)\\)");
                        Matcher m = p.matcher(line);
                        if (m.find()) {
                            machine.append(m.group(1)).append(" ");
                            
                            // Get register
                            Pattern regPattern = Pattern.compile("\\(RG,(\\d+)\\)");
                            Matcher regMatcher = regPattern.matcher(line);
                            if (regMatcher.find()) {
                                machine.append(regMatcher.group(1)).append(" ");
                            } else {
                                machine.append("0 ");
                            }

                            // Get operand (symbol or literal)
                            if (line.contains("(S,")) {
                                Pattern symPattern = Pattern.compile("\\(S,(\\d+)\\)");
                                Matcher symMatcher = symPattern.matcher(line);
                                if (symMatcher.find()) {
                                    int symIndex = Integer.parseInt(symMatcher.group(1));
                                    Symbol sym = symtab.get(symIndex);
                                    machine.append(sym != null ? sym.address : "0");
                                }
                            } else if (line.contains("(L,")) {
                                Pattern litPattern = Pattern.compile("\\(L,(\\d+)\\)");
                                Matcher litMatcher = litPattern.matcher(line);
                                if (litMatcher.find()) {
                                    int litIndex = Integer.parseInt(litMatcher.group(1));
                                    Literal lit = littab.get(litIndex);
                                    machine.append(lit != null ? lit.address : "0");
                                }
                            }
                        }
                    }
                    // Handle DL instructions
                    else if (line.contains("(DL,")) {
                        Pattern p = Pattern.compile("\\(C,(\\d+)\\)");
                        Matcher m = p.matcher(line);
                        if (m.find()) {
                            machine.append("00 0 ").append(m.group(1));
                        } else {
                            machine.append("00 0 0");
                        }
                    }

                    if (machine.length() > 0) {
                        bw.write(addr + "\t" + machine.toString().trim() + "\n");
                    }
                }
            }
        }
    }
}
