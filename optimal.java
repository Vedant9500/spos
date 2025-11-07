import java.util.*;

public class OptimalPageReplacement {

    public static void optimalPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        int pageFaults = 0;

        for (int i = 0; i < pages.length; i++) {
            int page = pages[i];

            if (!frames.contains(page)) {
                pageFaults++;
                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    // Find the page to replace
                    int indexToReplace = -1;
                    int farthestUse = -1;

                    for (int j = 0; j < frames.size(); j++) {
                        int f = frames.get(j);
                        int nextUse = Integer.MAX_VALUE;

                        // Check future uses
                        for (int k = i + 1; k < pages.length; k++) {
                            if (pages[k] == f) {
                                nextUse = k;
                                break;
                            }
                        }

                        if (nextUse > farthestUse) {
                            farthestUse = nextUse;
                            indexToReplace = j;
                        }
                    }
                    frames.set(indexToReplace, page);
                }
            }
            System.out.println("Frames after accessing " + page + ": " + frames);
        }

        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

    public static void main(String[] args) {
        int[] pages = {2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2};
        int frameSize = 3;

        optimalPageReplacement(pages, frameSize);
    }
}
