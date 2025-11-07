import java.util.*;

public class FIFOPageReplacement {

    public static void fifoPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        int pageFaults = 0;

        System.out.println("\n--- FIFO Page Replacement ---");

        for (int page : pages) {
            if (!frames.contains(page)) {
                pageFaults++;

                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    frames.remove(0);   // FIFO remove oldest
                    frames.add(page);
                }
            }
            System.out.println("Page: " + page + "  ->  Frames: " + frames);
        }

        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input frame size
        System.out.print("Enter number of frames: ");
        int frameSize = sc.nextInt();

        // Input number of pages
        System.out.print("Enter number of pages: ");
        int n = sc.nextInt();

        int[] pages = new int[n];
        System.out.println("Enter page reference string:");
        for (int i = 0; i < n; i++) {
            pages[i] = sc.nextInt();
        }

        fifoPageReplacement(pages, frameSize);
    }
}
