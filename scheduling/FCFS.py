# ---------- FCFS (First Come First Serve) Scheduling ----------

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0


def fcfs(processes):
    # Sort by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    time = 0
    for p in processes:
        time = max(time, p.arrival_time)
        p.waiting_time = time - p.arrival_time
        time += p.burst_time
        p.turnaround_time = p.waiting_time + p.burst_time

    print("----- FCFS Scheduling -----")
    for p in processes:
        print(f"P{p.pid}  WT={p.waiting_time}  TT={p.turnaround_time}")


# ---------- MAIN FUNCTION ----------
if __name__ == "__main__":
    # Change input here |
    processes = [
        Process(1, 0, 5),
        Process(2, 1, 3),
        Process(3, 2, 8)
    ]

    fcfs(processes)
