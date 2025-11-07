# ---------- Priority (Non-Preemptive) Scheduling ----------

class PSProcess:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0


def priority_scheduling(processes):
    # Sort processes by arrival time first
    processes.sort(key=lambda p: p.arrival_time)

    time = 0
    completed = []

    while len(completed) < len(processes):
        highest = None

        # Find the process with the highest priority (lowest number)
        for p in processes:
            if p not in completed and p.arrival_time <= time:
                if highest is None or p.priority < highest.priority:
                    highest = p

        # If no process is ready yet, increase time
        if highest is None:
            time += 1
            continue

        highest.waiting_time = time - highest.arrival_time
        time += highest.burst_time
        highest.turnaround_time = highest.waiting_time + highest.burst_time

        completed.append(highest)

    # Display results
    print("----- Priority (Non-Preemptive) Scheduling -----")
    for p in processes:
        print(f"P{p.pid}  Priority={p.priority}  WT={p.waiting_time}  TT={p.turnaround_time}")


# ---------- MAIN FUNCTION ----------
if __name__ == "__main__":
    # Change input here |
    processes = [
        PSProcess(1, 0, 5, 2),
        PSProcess(2, 1, 3, 1),
        PSProcess(3, 2, 8, 3)
    ]

    priority_scheduling(processes)
