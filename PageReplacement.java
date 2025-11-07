import java.util.*;

public class PageReplacement {

    // ---------- FIFO Page Replacement ----------
    static void fifo(int pages[], int n, int capacity) {
        Queue<Integer> q = new LinkedList<>();
        HashSet<Integer> s = new HashSet<>();

        int pageFaults = 0, pageHits = 0;

        for (int i = 0; i < n; i++) {
            if (!s.contains(pages[i])) {
                // Page Fault
                if (s.size() == capacity) {
                    int removed = q.poll();
                    s.remove(removed);
                }
                s.add(pages[i]);
                q.add(pages[i]);
                pageFaults++;
            } else {
                // Page Hit
                pageHits++;
            }
            System.out.println("Page " + pages[i] + " => " + s);
        }

        double hitRatio = (double) pageHits / n;
        double faultRatio = (double) pageFaults / n;

        System.out.println("Total Page Faults (FIFO): " + pageFaults);
        System.out.println("Total Page Hits (FIFO): " + pageHits);
        System.out.printf("Hit Ratio (FIFO): %.2f\n", hitRatio);
        System.out.printf("Fault Ratio (FIFO): %.2f\n", faultRatio);
    }

    // ---------- LRU Page Replacement ----------
    static void lru(int pages[], int n, int capacity) {
        HashSet<Integer> s = new HashSet<>(capacity);
        HashMap<Integer, Integer> indexes = new HashMap<>();

        int pageFaults = 0, pageHits = 0;

        for (int i = 0; i < n; i++) {
            if (s.contains(pages[i])) {
                pageHits++;
            } else {
                if (s.size() < capacity) {
                    s.add(pages[i]);
                    pageFaults++;
                } else {
                    int lru = Integer.MAX_VALUE, val = Integer.MIN_VALUE;

                    for (int page : s) {
                        if (indexes.get(page) < lru) {
                            lru = indexes.get(page);
                            val = page;
                        }
                    }

                    s.remove(val);
                    s.add(pages[i]);
                    pageFaults++;
                }
            }
            indexes.put(pages[i], i);
            System.out.println("Page " + pages[i] + " => " + s);
        }

        double hitRatio = (double) pageHits / n;
        double faultRatio = (double) pageFaults / n;

        System.out.println("Total Page Faults (LRU): " + pageFaults);
        System.out.println("Total Page Hits (LRU): " + pageHits);
        System.out.printf("Hit Ratio (LRU): %.2f\n", hitRatio);
        System.out.printf("Fault Ratio (LRU): %.2f\n", faultRatio);
    }

    // ---------- OPTIMAL Page Replacement ----------
    static void optimal(int pages[], int n, int capacity) {
        List<Integer> frames = new ArrayList<>(capacity);
        int pageFaults = 0, pageHits = 0;

        for (int i = 0; i < n; i++) {
            if (frames.contains(pages[i])) {
                pageHits++;
            } else {
                if (frames.size() < capacity) {
                    frames.add(pages[i]);
                } else {
                    int farthest = i + 1, replaceIndex = -1;
                    for (int j = 0; j < frames.size(); j++) {
                        int nextUse = Integer.MAX_VALUE;
                        for (int k = i + 1; k < n; k++) {
                            if (frames.get(j) == pages[k]) {
                                nextUse = k;
                                break;
                            }
                        }
                        if (nextUse > farthest) {
                            farthest = nextUse;
                            replaceIndex = j;
                        }
                    }
                    if (replaceIndex == -1)
                        replaceIndex = 0;
                    frames.set(replaceIndex, pages[i]);
                }
                pageFaults++;
            }
            System.out.println("Page " + pages[i] + " => " + frames);
        }

        double hitRatio = (double) pageHits / n;
        double faultRatio = (double) pageFaults / n;

        System.out.println("Total Page Faults (Optimal): " + pageFaults);
        System.out.println("Total Page Hits (Optimal): " + pageHits);
        System.out.printf("Hit Ratio (Optimal): %.2f\n", hitRatio);
        System.out.printf("Fault Ratio (Optimal): %.2f\n", faultRatio);
    }

    // ---------- MAIN FUNCTION ----------
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of pages: ");
        int n = sc.nextInt();
        int pages[] = new int[n];
        System.out.println("Enter the page reference string:");
        for (int i = 0; i < n; i++)
            pages[i] = sc.nextInt();

        System.out.print("Enter number of frames: ");
        int capacity = sc.nextInt();

        System.out.println("\n--- FIFO Page Replacement ---");
        fifo(pages, n, capacity);

        System.out.println("\n--- LRU Page Replacement ---");
        lru(pages, n, capacity);

        System.out.println("\n--- Optimal Page Replacement ---");
        optimal(pages, n, capacity);

        sc.close();
    }
}
