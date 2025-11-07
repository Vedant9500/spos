# ---------- Round Robin Scheduling ----------

from collections import deque

class RRProcess:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0


def round_robin(processes, quantum):
    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    time = 0
    i = 0
    n = len(processes)
    q = deque()

    # Add first process to queue
    q.append(processes[0])
    i = 1

    while q:
        p = q.popleft()

        exec_time = min(quantum, p.remaining_time)
        p.remaining_time -= exec_time
        time += exec_time

        # Add newly arrived processes to queue
        while i < n and processes[i].arrival_time <= time:
            q.append(processes[i])
            i += 1

        if p.remaining_time > 0:
            q.append(p)
        else:
            p.turnaround_time = time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

    # Display results
    print("----- Round Robin Scheduling -----")
    for p in processes:
        print(f"P{p.pid}  WT={p.waiting_time}  TT={p.turnaround_time}")


# ---------- MAIN FUNCTION ----------
if __name__ == "__main__":
    quantum = 3  # Time Quantum

    # Change inputs here |
    processes = [
        RRProcess(1, 0, 5),
        RRProcess(2, 1, 3),
        RRProcess(3, 2, 6)
    ]

    round_robin(processes, quantum)
