import java.util.*;

public class OptimalPageReplacement {

    public static void optimalPageReplacement(int[] pages, int frameSize) {
        List<Integer> frames = new ArrayList<>();
        int pageFaults = 0;

        System.out.println("\n--- Optimal Page Replacement ---");

        for (int i = 0; i < pages.length; i++) {
            int page = pages[i];

            if (!frames.contains(page)) {
                pageFaults++;

                if (frames.size() < frameSize) {
                    frames.add(page);
                } else {
                    int indexToReplace = -1;
                    int farthestUse = -1;

                    // Find the page used farthest in the future
                    for (int f = 0; f < frames.size(); f++) {
                        int currentPage = frames.get(f);
                        int nextUse = Integer.MAX_VALUE;

                        // Check when the current frame page will be used next
                        for (int j = i + 1; j < pages.length; j++) {
                            if (pages[j] == currentPage) {
                                nextUse = j;
                                break;
                            }
                        }

                        // The page not used for the longest time (or never used) will be replaced
                        if (nextUse > farthestUse) {
                            farthestUse = nextUse;
                            indexToReplace = f;
                        }
                    }

                    frames.set(indexToReplace, page);
                }
            }

            System.out.println("Page: " + page + "  ->  Frames: " + frames);
        }

        System.out.println("\nTotal Page Faults: " + pageFaults);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Frame size input
        System.out.print("Enter number of frames: ");
        int frameSize = sc.nextInt();

        // Number of pages input
        System.out.print("Enter number of pages: ");
        int n = sc.nextInt();

        int[] pages = new int[n];

        // Page reference string
        System.out.println("Enter page reference string:");
        for (int i = 0; i < n; i++) {
            pages[i] = sc.nextInt();
        }

        optimalPageReplacement(pages, frameSize);
    }
}
