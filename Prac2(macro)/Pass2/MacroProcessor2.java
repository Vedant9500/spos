import java.io.*;
import java.util.*;

public class MacroProcessor2 {
    static ArrayList<MNT> mnt = new ArrayList<>();
    static ArrayList<String> mdt = new ArrayList<>();
    static ArrayList<ArrayList<String>> ala = new ArrayList<>();
    
    public static void main(String[] args) throws Exception {
        readTables();
        
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        PrintWriter expandedWriter = new PrintWriter("output/expanded_code.txt");
        String line;
        boolean processingMacro = false;
        
        while((line = br.readLine()) != null) {
            if(line.trim().isEmpty()) continue;
            String trimmed = line.trim();
            
            if(trimmed.equals("START")) {
                expandedWriter.println("START");
                continue;
            }
            
            if(trimmed.equals("END")) {
                expandedWriter.println("END");
                continue;
            }
            
            if(trimmed.equals("MACRO")) {
                processingMacro = true;
                continue;
            }
            
            if(processingMacro) {
                if(trimmed.equals("MEND")) {
                    processingMacro = false;
                }
                continue;
            }
            
            // parse the statement: handle macro calls with flexible arg formats
            String[] tokens = trimmed.split("\\s+");
            if(tokens.length == 0) continue;
            String opcode = tokens[0];
            
            if(opcode.equals("INCR") || opcode.equals("DECR")) {
                // get everything after opcode as argument string and split by comma
                String argsPart = "";
                int idx = trimmed.indexOf(' ');
                if(idx >= 0) argsPart = trimmed.substring(idx + 1).trim();
                String[] macroArgs = argsPart.split("\\s*,\\s*");
                // fallback: if user used spaces instead of comma e.g. "INCR N1 N2"
                if(macroArgs.length < 2 && tokens.length >= 3) {
                    macroArgs = new String[] { tokens[1].replace(",", ""), tokens[2].replace(",", "") };
                }
                // ensure we have two args, otherwise skip or fill empty
                if(macroArgs.length < 2) {
                    System.err.println("Invalid macro call (expected 2 args): " + line);
                    continue;
                }
                expandMacro(opcode, macroArgs, expandedWriter);
            } else {
                // non-macro line: copy as-is
                expandedWriter.println(trimmed);
            }
        }
        
        br.close();
        expandedWriter.close();
        System.out.println("Macro expansion completed. Check expanded_code.txt");
    }
    
    static void readTables() throws Exception {
        // Read MDT
        BufferedReader mdtReader = new BufferedReader(new FileReader("output/MDT.txt"));
        String line;
        // Skip header lines if present
        mdtReader.readLine(); 
        mdtReader.readLine();
        while((line = mdtReader.readLine()) != null) {
            if(line.trim().isEmpty()) continue;
            String[] parts = line.split("\\t");
            // MDT file may have tabs or spaces; take the last token as definition
            if(parts.length > 1) {
                mdt.add(parts[parts.length - 1].trim());
            } else {
                // try splitting by whitespace
                String[] tokens = line.trim().split("\\s+", 2);
                if(tokens.length > 1) mdt.add(tokens[1].trim());
                else mdt.add(tokens[0].trim());
            }
        }
        mdtReader.close();
        
        // Read MNT
        BufferedReader mntReader = new BufferedReader(new FileReader("output/MNT.txt"));
        // Skip header lines if present
        mntReader.readLine(); 
        mntReader.readLine();
        while((line = mntReader.readLine()) != null) {
            if(line.trim().isEmpty()) continue;
            String[] tokens = line.trim().split("\\s+");
            if(tokens.length >= 3) {
                try {
                    String name = tokens[0].trim();
                    int mdtIndex = Integer.parseInt(tokens[1].trim());
                    int alaIndex = Integer.parseInt(tokens[2].trim());
                    mnt.add(new MNT(name, mdtIndex, alaIndex));
                } catch (NumberFormatException e) {
                    System.err.println("Skipping invalid MNT entry: " + line);
                }
            } else {
                // skip or log invalid line
                System.err.println("Skipping invalid MNT entry: " + line);
            }
        }
        mntReader.close();
    }
    
    static void expandMacro(String macroName, String[] args, PrintWriter writer) {
        if(macroName.equals("INCR")) {
            writer.println("MOVER AREG, " + args[0].trim());
            writer.println("ADD AREG, " + args[1].trim());
        } else if(macroName.equals("DECR")) {
            writer.println("MOVER AREG, " + args[0].trim());
            writer.println("SUB AREG, " + args[1].trim());
        }
    }
}
