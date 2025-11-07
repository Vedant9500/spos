import java.util.*;

public class LRUPageReplacement {

    public static void lruPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        Map<Integer, Integer> recentUsage = new HashMap<>(); // Tracks last usage index
        int pageFaults = 0;

        for (int i = 0; i < pages.length; i++) {
            int page = pages[i];

            if (!frames.contains(page)) {
                pageFaults++;
                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    // Find the least recently used page in frames
                    int lruPage = frames.get(0);
                    int minUsage = Integer.MAX_VALUE;

                    for (int f : frames) {
                        int lastUsed = recentUsage.getOrDefault(f, -1);
                        if (lastUsed < minUsage) {
                            minUsage = lastUsed;
                            lruPage = f;
                        }
                    }

                    // Replace LRU page
                    int lruIndex = frames.indexOf(lruPage);
                    frames.set(lruIndex, page);
                }
            }

            // Update last usage of current page
            recentUsage.put(page, i);

            System.out.println("Frames after accessing " + page + ": " + frames);
        }

        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

    public static void main(String[] args) {
        int[] pages = {2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2};
        int frameSize = 3;

        lruPageReplacement(pages, frameSize);
    }
}
