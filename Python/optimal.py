# Optimal Page Replacement Algorithm in Python

def optimal_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0

    for i in range(len(pages)):
        page = pages[i]

        if page not in frames:
            page_faults += 1
            if len(frames) < frame_size:
                frames.append(page)
            else:
                # Find the page to replace
                future_uses = []
                for f in frames:
                    if f in pages[i+1:]:
                        future_uses.append(pages[i+1:].index(f))
                    else:
                        # If page is not used again, replace it immediately
                        future_uses.append(float('inf'))
                
                # Replace the page that is used farthest in the future
                index_to_replace = future_uses.index(max(future_uses))
                frames[index_to_replace] = page
        print(f"Frames after accessing {page}: {frames}")

    print(f"\nTotal Page Faults: {page_faults}")

# Sample input
pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3

optimal_page_replacement(pages, frame_size)
