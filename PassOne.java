import java.io.*;
import java.util.*;

class Symbol {
    String name;
    int address;
    Symbol(String n, int a) { name = n; address = a; }
}

class Literal {
    String value;
    int address;
    Literal(String v, int a) { value = v; address = a; }
}

public class PassOne {
    static Map<String, Integer> MOT = new HashMap<>();
    static Map<String, Integer> REG = new HashMap<>();
    static List<Symbol> SYMTAB = new ArrayList<>();
    static List<Literal> LITTAB = new ArrayList<>();
    static List<Integer> POOLTAB = new ArrayList<>(); 
    static List<String> IC = new ArrayList<>();

    static int LC = 0;
    static int lastLitIndex = 0;

    public static void main(String[] args) throws Exception {
        MOT.put("STOP", 0); MOT.put("ADD", 1); MOT.put("SUB", 2);
        MOT.put("MULT", 3); MOT.put("MOVER", 4); MOT.put("MOVEM", 5);
        MOT.put("BC", 6);
        MOT.put("LTORG", -1); MOT.put("START", -2); MOT.put("END", -3);
        MOT.put("ORIGIN", -4); MOT.put("EQU", -5); MOT.put("DS", -6);

        REG.put("AREG", 1); REG.put("BREG", 2); REG.put("CREG", 3);

        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.equals("")) continue;
                String[] p = line.split("[ ,]+");
                String label = "", op = "", op1 = "", op2 = "";
                int idx = 0;
                if (!MOT.containsKey(p[0])) { label = p[0]; idx = 1; }
                if (idx < p.length) op = p[idx++];
                if (idx < p.length) op1 = p[idx++];
                if (idx < p.length) op2 = p[idx++];
                
                if (!label.isEmpty()) {
                    if (!op.equals("EQU")) addOrUpdateSymbol(label, LC);
                    else addOrUpdateSymbol(label, -1);
                }
                
                switch (op) {
                    case "START" -> {
                        LC = (op1 != null && !op1.isEmpty()) ? Integer.parseInt(op1) : 0;
                        addIC(LC, "(AD,START) (C," + LC + ")");
                    }
                    case "ORIGIN" -> {
                        LC = evaluate(op1);
                        addIC(LC, "(AD,ORIGIN) (C," + LC + ")");
                    }
                    case "EQU" -> {
                        int addr = evaluate(op1);
                        int symIndex = getSymIndex(label);
                        SYMTAB.get(symIndex).address = addr;
                        addIC(LC, "(AD,EQU) (S," + (symIndex+1) + ") (C," + addr + ")");
                    }
                    case "LTORG", "END" -> {
                        if (lastLitIndex < LITTAB.size()) {
                            POOLTAB.add(lastLitIndex + 1);
                            addIC(LC, "(AD,LTORG)");
                            for (int i = lastLitIndex; i < LITTAB.size(); i++) {
                                LITTAB.get(i).address = LC++;
                                addIC(LITTAB.get(i).address, "(DL,01) (C," + literalValueNumber(LITTAB.get(i).value) + ")");
                            }
                            lastLitIndex = LITTAB.size();
                        } else {
                            addIC(LC, "(AD,LTORG)");
                        }
                        if (op.equals("END")) addIC(LC, "(AD,END)");
                    }
                    case "DS" -> {
                        int si = getSymIndex(label);
                        SYMTAB.get(si).address = LC;
                        addIC(LC, "(DL,DS) (C," + op1 + ")");
                        LC += Integer.parseInt(op1);
                    }
                    default -> {
                        if (MOT.containsKey(op) && MOT.get(op) >= 0) {
                            int motCode = MOT.get(op);
                            String regCode = "0";
                            if (!op1.isEmpty() && REG.containsKey(op1)) regCode = REG.get(op1).toString();
                            if (!op2.isEmpty() && isLiteral(op2)) {
                                LITTAB.add(new Literal(op2, -1));
                                int litIndex = LITTAB.size();
                                addIC(LC, "(IS," + String.format("%02d", motCode) + ") (RG," + regCode + ") (L," + litIndex + ")");
                            } else if (!op2.isEmpty()) {
                                int symIdx = getSymIndex(op2);
                                addIC(LC, "(IS," + String.format("%02d", motCode) + ") (RG," + regCode + ") (S," + (symIdx+1) + ")");
                            } else {
                                addIC(LC, "(IS," + String.format("%02d", motCode) + ") (RG," + regCode + ")");
                            }
                            LC++;
                        }
                    }
                }
            }
        }

        // print to console
        printTables();
        // write each table to its own file
        writeSymbolTableFile("symbol_table.txt");
        writeLiteralTableFile("literal_table.txt");
        writePoolTableFile("pool_table.txt");
        writeIntermediateFile("intermediate_code.txt");
        System.out.println("\nFiles written: symbol_table.txt, literal_table.txt, pool_table.txt, intermediate_code.txt");
    }

    static boolean isLiteral(String op) {
        return op.startsWith("=");
    }

    static int literalValueNumber(String lit) {
        if (lit == null) return 0;
        String t = lit.trim();
        if (t.startsWith("=")) t = t.substring(1);
        t = t.replaceAll("['\"]", "");
        try {
            return Integer.parseInt(t);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    static void addOrUpdateSymbol(String sym, int addr) {
        for (Symbol s : SYMTAB) {
            if (s.name.equals(sym)) {
                if (addr >= 0) s.address = addr;
                return;
            }
        }
        SYMTAB.add(new Symbol(sym, addr));
    }

    static int getSymIndex(String sym) {
        for (int i = 0; i < SYMTAB.size(); i++) {
            if (SYMTAB.get(i).name.equals(sym)) return i;
        }
        SYMTAB.add(new Symbol(sym, -1));
        return SYMTAB.size() - 1;
    }

    static int getSymbolAddr(String sym) {
        for (Symbol s : SYMTAB)
            if (s.name.equals(sym)) return s.address;
        return -1;
    }

    static int evaluate(String expr) {
        expr = expr.trim();
        if (expr.matches("\\d+")) return Integer.parseInt(expr);
        if (expr.contains("+")) {
            String[] t = expr.split("\\+");
            int base = getSymbolAddr(t[0]);
            int off = Integer.parseInt(t[1]);
            return (base >= 0 ? base : 0) + off;
        } else if (expr.contains("-")) {
            String[] t = expr.split("-");
            int base = getSymbolAddr(t[0]);
            int off = Integer.parseInt(t[1]);
            return (base >= 0 ? base : 0) - off;
        } else {
            int a = getSymbolAddr(expr);
            return (a >= 0) ? a : 0;
        }
    }

    static void addIC(int lc, String code) {
        IC.add(lc + " : " + code);
    }

    static void printTables() {
        System.out.println("\n--- SYMBOL TABLE ---");
        int i = 1;
        for (Symbol s : SYMTAB)
            System.out.println(i++ + "\t" + s.name + "\t" + s.address);

        System.out.println("\n--- LITERAL TABLE ---");
        i = 1;
        for (Literal l : LITTAB)
            System.out.println(i++ + "\t" + l.value + "\t" + l.address);

        System.out.println("\n--- POOL TABLE ---");
        i = 1;
        for (Integer p : POOLTAB)
            System.out.println("#" + i++ + "\t" + p);

        System.out.println("\n--- INTERMEDIATE CODE ---");
        for (String s : IC)
            System.out.println(s);
    }

    static void writeSymbolTableFile(String fname) throws IOException {
        try (BufferedWriter w = new BufferedWriter(new FileWriter(fname))) {
            w.write("Index\tSymbol\tAddress\n");
            int i = 1;
            for (Symbol s : SYMTAB) {
                w.write(i++ + "\t" + s.name + "\t" + s.address + "\n");
            }
        }
    }

    static void writeLiteralTableFile(String fname) throws IOException {
        try (BufferedWriter w = new BufferedWriter(new FileWriter(fname))) {
            w.write("Index\tLiteral\tAddress\n");
            int i = 1;
            for (Literal l : LITTAB) {
                w.write(i++ + "\t" + l.value + "\t" + l.address + "\n");
            }
        }
    }

    static void writePoolTableFile(String fname) throws IOException {
        try (BufferedWriter w = new BufferedWriter(new FileWriter(fname))) {
            w.write("PoolIndex\tStartLiteralIndex\n");
            int i = 1;
            for (Integer p : POOLTAB) {
                w.write("#" + i++ + "\t" + p + "\n");
            }
        }
    }

    static void writeIntermediateFile(String fname) throws IOException {
        try (BufferedWriter w = new BufferedWriter(new FileWriter(fname))) {
            for (String s : IC) w.write(s + "\n");
        }
    }
}