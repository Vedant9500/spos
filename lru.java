import java.util.*;

public class LRUPageReplacement {

    public static void lruPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        Map<Integer, Integer> recentUse = new HashMap<>();
        int pageFaults = 0;

        System.out.println("\n--- LRU Page Replacement ---");

        for (int i = 0; i < pages.length; i++) {
            int page = pages[i];

            if (!frames.contains(page)) {
                pageFaults++;

                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    // Find least recently used page
                    int lruPage = frames.get(0);
                    for (int p : frames) {
                        if (recentUse.get(p) < recentUse.get(lruPage)) {
                            lruPage = p;
                        }
                    }
                    frames.remove(Integer.valueOf(lruPage));
                    frames.add(page);
                }
            }

            // Update recent use time
            recentUse.put(page, i);

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

        lruPageReplacement(pages, frameSize);
    }
}
