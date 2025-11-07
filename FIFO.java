import java.util.*;

public class FIFOPageReplacement {
    
    public static void fifoPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        int pageFaults = 0;

        for (int page : pages) {
            if (!frames.contains(page)) {
                // Page fault occurs
                pageFaults++;
                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    // Remove the oldest page (FIFO)
                    frames.remove(0);
                    frames.add(page);
                }
            }
            System.out.println("Frames: " + frames);
        }

        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

    public static void main(String[] args) {
        int[] pages = {2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2};
        int frameSize = 3;

        fifoPageReplacement(pages, frameSize);
    }
}
