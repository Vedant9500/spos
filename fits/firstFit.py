# ---------- First Fit Memory Allocation ----------

def first_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)  # Initialize allocation list

    print("----- First Fit Allocation -----")

    for i in range(len(process_sizes)):
        for j in range(len(memory_blocks)):
            if memory_blocks[j] >= process_sizes[i]:
                allocation[i] = j
                memory_blocks[j] -= process_sizes[i]
                print(
                    f"Process {i} (size {process_sizes[i]}) allocated to Block {j} "
                    f"(remaining {memory_blocks[j]})"
                )
                break  # Move to the next process once allocated

        if allocation[i] == -1:
            print(f"Process {i} (size {process_sizes[i]}) NOT allocated.")


# ---------- MAIN FUNCTION ----------

if __name__ == "__main__":
    # You can modify inputs here
    memory_blocks = [100, 500, 200, 300, 600]
    process_sizes = [212, 417, 112, 426]

    first_fit(memory_blocks, process_sizes)
