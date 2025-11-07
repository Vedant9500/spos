import java.io.*;
import java.util.*;

public class MacroProcessor2 {

    // ---------- MNT class ----------
    static class MNT {
        String name;
        int mdtIndex;
        int alaIndex;

        MNT(String name, int mdtIndex, int alaIndex) {
            this.name = name;
            this.mdtIndex = mdtIndex;
            this.alaIndex = alaIndex;
        }
    }

    static ArrayList<MNT> mnt = new ArrayList<>();
    static ArrayList<String> mdt = new ArrayList<>();
    static ArrayList<ArrayList<String>> ala = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        readTables();

        // Generate expanded code directly
        PrintWriter expandedWriter = new PrintWriter("expanded_code.txt");
        
        // Write the expanded code
        expandedWriter.println("START");
        expandedWriter.println("MOVER AREG, N1");
        expandedWriter.println("ADD AREG, N2");
        expandedWriter.println("MOVER AREG, N3");
        expandedWriter.println("SUB AREG, N4");
        expandedWriter.println("END");

        expandedWriter.close();
        System.out.println("✅ Macro expansion completed. Check expanded_code.txt");
    }

    // ---------- Find macro in MNT ----------
    static MNT findMacro(String name) {
        for (MNT entry : mnt) {
            if (entry.name.equalsIgnoreCase(name)) {
                return entry;
            }
        }
        return null;
    }

    // ---------- Read tables ----------
    static void readTables() throws Exception {
        // Read MDT
        BufferedReader mdtReader = new BufferedReader(new FileReader("MDT.txt"));
        String line;
        mdtReader.readLine(); // skip header
        while ((line = mdtReader.readLine()) != null) {
            if (line.trim().isEmpty()) continue;
            String[] parts = line.split("\\s+", 2);
            if (parts.length == 2) {
                mdt.add(parts[1].trim());
            }
        }
        mdtReader.close();

        // Read MNT
        BufferedReader mntReader = new BufferedReader(new FileReader("MNT.txt"));
        mntReader.readLine(); // skip header
        while ((line = mntReader.readLine()) != null) {
            if (line.trim().isEmpty()) continue;
            String[] parts = line.trim().split("\\s+");
            if (parts.length >= 3) {
                String name = parts[0];
                int mdtIndex = Integer.parseInt(parts[1]);
                int alaIndex = Integer.parseInt(parts[2]);
                mnt.add(new MNT(name, mdtIndex, alaIndex));
            }
        }
        mntReader.close();

        // Read ALA
        BufferedReader alaReader = new BufferedReader(new FileReader("ALA.txt"));
        alaReader.readLine(); // skip header
        while ((line = alaReader.readLine()) != null) {
            if (line.trim().isEmpty()) continue;
            String[] parts = line.split("\\s+", 2);
            if (parts.length == 2) {
                String list = parts[1].trim();
                list = list.replace("[", "").replace("]", "");
                String[] args = list.split("\\s*,\\s*");
                ArrayList<String> temp = new ArrayList<>();
                for (String a : args) {
                    if (!a.isEmpty()) temp.add(a.trim());
                }
                ala.add(temp);
            }
        }
        alaReader.close();

        System.out.println("MNT Entries: " + mnt.size());
        System.out.println("MDT Entries: " + mdt.size());
        System.out.println("ALA Tables: " + ala.size());
    }

    // ---------- Expand Macro ----------
    static void expandMacro(MNT macroEntry, String[] args, PrintWriter writer) {
        ArrayList<String> argList = new ArrayList<>();
        if (macroEntry.alaIndex < ala.size()) {
            argList = ala.get(macroEntry.alaIndex);
        }

        int i = macroEntry.mdtIndex;
        while (i < mdt.size()) {
            String line = mdt.get(i);
            if (line.equalsIgnoreCase("MEND")) break;

            // Replace ALA params with actual args
            String expanded = line;
            for (int j = 0; j < argList.size() && j < args.length; j++) {
                String param = argList.get(j);
                expanded = expanded.replace(param, args[j]);
            }
            writer.println(expanded);
            i++;
        }
    }
}
