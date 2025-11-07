# ---------- SJF Preemptive (Shortest Remaining Time First) Scheduling ----------

class SJFProcess:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0


def sjf_preemptive(processes):
    time = 0
    completed = 0
    n = len(processes)

    while completed < n:
        shortest = None

        # Find the process with the shortest remaining time among arrived ones
        for p in processes:
            if p.arrival_time <= time and p.remaining_time > 0:
                if shortest is None or p.remaining_time < shortest.remaining_time:
                    shortest = p

        if shortest is None:
            time += 1
            continue

        # Execute for 1 unit of time
        shortest.remaining_time -= 1
        time += 1

        # Process completes
        if shortest.remaining_time == 0:
            completed += 1
            shortest.turnaround_time = time - shortest.arrival_time
            shortest.waiting_time = shortest.turnaround_time - shortest.burst_time

    # Display results
    print("----- SJF Preemptive (SRTF) Scheduling -----")
    total_wt = 0
    total_tt = 0

    for p in processes:
        total_wt += p.waiting_time
        total_tt += p.turnaround_time
        print(f"P{p.pid} | WT = {p.waiting_time} | TT = {p.turnaround_time}")

    # Calculate averages
    avg_wt = total_wt / n
    avg_tt = total_tt / n

    print("\nAverage Waiting Time =", round(avg_wt, 2))
    print("Average Turnaround Time =", round(avg_tt, 2))


# ---------- MAIN ----------
if __name__ == "__main__":
    # Change inputs here
    processes = [
        SJFProcess(1, 0, 7),
        SJFProcess(2, 2, 4),
        SJFProcess(3, 4, 1),
        SJFProcess(4, 5, 4)
    ]

    sjf_preemptive(processes)
