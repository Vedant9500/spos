import java.io.*;
import java.util.*;

class MNT {
    String name;
    int mdtIndex;
    int alaIndex;
    
    public MNT(String name, int mdtIndex, int alaIndex) {
        this.name = name;
        this.mdtIndex = mdtIndex;
        this.alaIndex = alaIndex;
    }
}

public class MacroProcessor1 {
    static ArrayList<MNT> mnt = new ArrayList<>();
    static ArrayList<String> mdt = new ArrayList<>();
    static ArrayList<ArrayList<String>> ala = new ArrayList<>();
    
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        String line;
        boolean isMacro = false;
        int mdtIndex = 0;
        int currentALA = -1;
        
        while((line = br.readLine()) != null) {
            String[] parts = line.trim().split("\\s+");
            
            if(parts[0].equals("MACRO")) {
                isMacro = true;
                continue;
            }
            
            if(isMacro) {
                if(parts[0].equals("MEND")) {
                    mdt.add("MEND");
                    mdtIndex++;
                    isMacro = false;
                    continue;
                }
                
                if(!parts[0].equals("MEND")) {
                    if(parts[0].equals("INCR")) {
                        mdt.add(line);
                        mdt.add("MOVER AREG, " + parts[1].replace("&", ""));
                        mdt.add("ADD AREG, " + parts[2].replace("&", ""));
                        mdtIndex += 3;
                        
                        ArrayList<String> arguments = new ArrayList<>();
                        for(String part : parts) {
                            if(part.contains("&")) {
                                arguments.add(part);
                            }
                        }
                        ala.add(arguments);
                        mnt.add(new MNT("INCR", mdtIndex-3, currentALA+1));
                        currentALA++;
                    }
                    else if(parts[0].equals("DECR")) {
                        mdt.add(line);
                        mdt.add("MOVER AREG, " + parts[1].replace("&", ""));
                        mdt.add("SUB AREG, " + parts[2].replace("&", ""));
                        mdtIndex += 3;
                        
                        ArrayList<String> arguments = new ArrayList<>();
                        for(String part : parts) {
                            if(part.contains("&")) {
                                arguments.add(part);
                            }
                        }
                        ala.add(arguments);
                        mnt.add(new MNT("DECR", mdtIndex-3, currentALA+1));
                        currentALA++;
                    }
                }
            }
        }
        
        displayTables();
        br.close();
    }
    
    static void displayTables() {
        try {
            // Create output directory if it doesn't exist
            File outputDir = new File("output");
            if (!outputDir.exists()) {
                outputDir.mkdir();
            }

            // Write MNT to file
            PrintWriter mntWriter = new PrintWriter("output/MNT.txt");
            mntWriter.println("Macro Name Table (MNT):");
            mntWriter.println("Name\tMDT Index\tALA Index");
            for(MNT entry : mnt) {
                mntWriter.println(entry.name + "\t" + entry.mdtIndex + "\t\t" + entry.alaIndex);
            }
            mntWriter.close();

            // Write MDT to file
            PrintWriter mdtWriter = new PrintWriter("output/MDT.txt");
            mdtWriter.println("Macro Definition Table (MDT):");
            mdtWriter.println("Index\tDefinition");
            for(int i = 0; i < mdt.size(); i++) {
                mdtWriter.println(i + "\t" + mdt.get(i));
            }
            mdtWriter.close();

            // Write ALA to file
            PrintWriter alaWriter = new PrintWriter("output/ALA.txt");
            alaWriter.println("Argument List Array (ALA):");
            alaWriter.println("Index\tArguments");
            for(int i = 0; i < ala.size(); i++) {
                alaWriter.println(i + "\t" + ala.get(i));
            }
            alaWriter.close();

            System.out.println("Output files have been created in the 'output' folder");
        } catch (FileNotFoundException e) {
            System.err.println("Error writing to output files: " + e.getMessage());
        }
    }
}
