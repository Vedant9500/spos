from collections import deque

# ---------- FIFO Page Replacement ----------
def fifo(pages, n, capacity):
    q = deque()
    s = set()

    page_faults = 0
    page_hits = 0

    for i in range(n):
        if pages[i] not in s:
            # Page Fault
            if len(s) == capacity:
                removed = q.popleft()
                s.remove(removed)
            s.add(pages[i])
            q.append(pages[i])
            page_faults += 1
        else:
            # Page Hit
            page_hits += 1

        print(f"Page {pages[i]} => {list(s)}")

    hit_ratio = page_hits / n
    fault_ratio = page_faults / n

    print(f"Total Page Faults (FIFO): {page_faults}")
    print(f"Total Page Hits (FIFO): {page_hits}")
    print(f"Hit Ratio (FIFO): {hit_ratio:.2f}")
    print(f"Fault Ratio (FIFO): {fault_ratio:.2f}")


# ---------- LRU Page Replacement ----------
def lru(pages, n, capacity):
    s = set()
    indexes = {}
    page_faults = 0
    page_hits = 0

    for i in range(n):
        if pages[i] in s:
            page_hits += 1
        else:
            if len(s) < capacity:
                s.add(pages[i])
                page_faults += 1
            else:
                # Find least recently used page
                lru = float('inf')
                val = None
                for page in s:
                    if indexes[page] < lru:
                        lru = indexes[page]
                        val = page
                s.remove(val)
                s.add(pages[i])
                page_faults += 1

        indexes[pages[i]] = i
        print(f"Page {pages[i]} => {list(s)}")

    hit_ratio = page_hits / n
    fault_ratio = page_faults / n

    print(f"Total Page Faults (LRU): {page_faults}")
    print(f"Total Page Hits (LRU): {page_hits}")
    print(f"Hit Ratio (LRU): {hit_ratio:.2f}")
    print(f"Fault Ratio (LRU): {fault_ratio:.2f}")


# ---------- OPTIMAL Page Replacement ----------
def optimal(pages, n, capacity):
    frames = []
    page_faults = 0
    page_hits = 0

    for i in range(n):
        if pages[i] in frames:
            page_hits += 1
        else:
            if len(frames) < capacity:
                frames.append(pages[i])
            else:
                farthest = i + 1
                replace_index = -1
                for j in range(len(frames)):
                    next_use = float('inf')
                    for k in range(i + 1, n):
                        if frames[j] == pages[k]:
                            next_use = k
                            break
                    if next_use > farthest:
                        farthest = next_use
                        replace_index = j
                if replace_index == -1:
                    replace_index = 0
                frames[replace_index] = pages[i]
            page_faults += 1

        print(f"Page {pages[i]} => {frames}")

    hit_ratio = page_hits / n
    fault_ratio = page_faults / n

    print(f"Total Page Faults (Optimal): {page_faults}")
    print(f"Total Page Hits (Optimal): {page_hits}")
    print(f"Hit Ratio (Optimal): {hit_ratio:.2f}")
    print(f"Fault Ratio (Optimal): {fault_ratio:.2f}")


# ---------- MAIN FUNCTION ----------
def main():
    n = int(input("Enter number of pages: "))
    pages = list(map(int, input("Enter the page reference string:\n").split()))
    if len(pages) != n:
        print("Error: Number of pages entered does not match input count!")
        return

    capacity = int(input("Enter number of frames: "))

    print("\n--- FIFO Page Replacement ---")
    fifo(pages, n, capacity)

    print("\n--- LRU Page Replacement ---")
    lru(pages, n, capacity)

    print("\n--- Optimal Page Replacement ---")
    optimal(pages, n, capacity)


if __name__ == "__main__":
    main()
