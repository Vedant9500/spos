# Corrected LRU Page Replacement Algorithm in Python

def lru_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    recent_usage = {}  # Tracks last usage of pages currently in frames

    for i, page in enumerate(pages):
        if page not in frames:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Consider only pages currently in frames for LRU
                lru_page = min({p: recent_usage[p] for p in frames}, key=lambda k: recent_usage[k])
                lru_index = frames.index(lru_page)
                frames[lru_index] = page
        # Update the last usage of the current page
        recent_usage[page] = i
        print(f"Frames after accessing {page}: {frames}")

    print(f"\nTotal Page Faults: {page_faults}")

# Sample input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3

lru_page_replacement(pages, frame_size)
