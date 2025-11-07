# ---------- Worst Fit Memory Allocation ----------

def worst_fit(memory_blocks, process_sizes):
    allocation = [-1] * len(process_sizes)

    print("----- Worst Fit Allocation -----")

    for i in range(len(process_sizes)):
        worst_idx = -1

        for j in range(len(memory_blocks)):
            if memory_blocks[j] >= process_sizes[i]:
                if worst_idx == -1 or memory_blocks[j] > memory_blocks[worst_idx]:
                    worst_idx = j

        if worst_idx != -1:
            allocation[i] = worst_idx
            memory_blocks[worst_idx] -= process_sizes[i]
            print(
                f"Process {i} (size {process_sizes[i]}) allocated to Block {worst_idx} "
                f"(remaining {memory_blocks[worst_idx]})"
            )
        else:
            print(f"Process {i} (size {process_sizes[i]}) NOT allocated.")


# ---------- MAIN FUNCTION ----------

if __name__ == "__main__":
    # Change inputs here as needed
    memory_blocks = [100, 500, 200, 300, 600]
    process_sizes = [212, 417, 112, 426]

    worst_fit(memory_blocks, process_sizes)
