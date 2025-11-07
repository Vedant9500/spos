# ---------- Best Fit Memory Allocation ----------

def best_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)  # Initialize allocation list

    print("----- Best Fit Allocation -----")

    for i in range(len(process_sizes)):
        best_idx = -1

        # Find the best fit block for the current process
        for j in range(len(memory_blocks)):
            if memory_blocks[j] >= process_sizes[i]:
                if best_idx == -1 or memory_blocks[j] < memory_blocks[best_idx]:
                    best_idx = j

        # If a suitable block was found
        if best_idx != -1:
            allocation[i] = best_idx
            memory_blocks[best_idx] -= process_sizes[i]
            print(
                f"Process {i} (size {process_sizes[i]}) allocated to Block {best_idx} "
                f"(remaining {memory_blocks[best_idx]})"
            )
        else:
            print(f"Process {i} (size {process_sizes[i]}) NOT allocated.")

# ---------- MAIN FUNCTION ----------

if __name__ == "__main__":
    # You can change inputs here
    memory_blocks = [100, 500, 200, 300, 600]
    process_sizes = [212, 417, 112, 426]

    best_fit(memory_blocks, process_sizes)
