# ---------- Next Fit Memory Allocation ----------

def next_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)
    last_ptr = 0  # To keep track of the last allocated block

    print("----- Next Fit Allocation -----")

    for i in range(len(process_sizes)):
        j = last_ptr
        allocated = False

        while True:
            if memory_blocks[j] >= process_sizes[i]:
                allocation[i] = j
                memory_blocks[j] -= process_sizes[i]
                last_ptr = j
                print(
                    f"Process {i} (size {process_sizes[i]}) allocated to Block {j} "
                    f"(remaining {memory_blocks[j]})"
                )
                allocated = True
                break

            j = (j + 1) % len(memory_blocks)

            # Stop if we have looped back to the starting point
            if j == last_ptr:
                break

        if not allocated:
            print(f"Process {i} (size {process_sizes[i]}) NOT allocated.")


# ---------- MAIN FUNCTION ----------

if __name__ == "__main__":
    # Change input values here if needed
    memory_blocks = [100, 500, 200, 300, 600]
    process_sizes = [212, 417, 112, 426]

    next_fit(memory_blocks, process_sizes)
