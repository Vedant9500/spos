# FIFO Page Replacement Algorithm in Python

# Function to simulate FIFO page replacement
def fifo_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0

    for page in pages:
        if page not in frames:
            # Page fault occurs
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Remove the oldest page (FIFO)
                frames.pop(0)
                frames.append(page)
        print(f"Frames: {frames}")  # Display current frames after each page reference

    print(f"\nTotal Page Faults: {page_faults}")


# Sample input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3

fifo_page_replacement(pages, frame_size)
