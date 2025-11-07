import java.util.*;

class SJFProcess {
    int pid, arrivalTime, burstTime;
    int remainingTime;
    int waitingTime, turnaroundTime;

    SJFProcess(int pid, int arrivalTime, int burstTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
        this.remainingTime = burstTime;
    }
}

// ✅ CLASS NAME CHANGED HERE
public class SJFChart {

    static class Segment {
        int pid, start, end;
        Segment(int pid, int start, int end) {
            this.pid = pid;
            this.start = start;
            this.end = end;
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        List<SJFProcess> processes = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            System.out.println("\nEnter details for Process " + (i + 1) + ":");

            System.out.print("Process ID: ");
            int pid = sc.nextInt();

            System.out.print("Arrival Time: ");
            int at = sc.nextInt();

            System.out.print("Burst Time: ");
            int bt = sc.nextInt();

            processes.add(new SJFProcess(pid, at, bt));
        }

        int time = 0, completed = 0;

        List<Segment> gantt = new ArrayList<>();
        Integer lastPID = null;
        int segmentStart = 0;

        // SRTF Simulation
        while (completed < n) {

            SJFProcess shortest = null;

            for (SJFProcess p : processes) {
                if (p.arrivalTime <= time && p.remainingTime > 0) {
                    if (shortest == null || p.remainingTime < shortest.remainingTime) {
                        shortest = p;
                    }
                }
            }

            if (shortest == null) {
                time++;
                continue;
            }

            // =====================
            // GANTT CHART TRACKING
            // =====================
            if (lastPID == null) {
                lastPID = shortest.pid;
                segmentStart = time;
            } else if (lastPID != shortest.pid) {
                gantt.add(new Segment(lastPID, segmentStart, time));
                lastPID = shortest.pid;
                segmentStart = time;
            }

            shortest.remainingTime--;
            time++;

            if (shortest.remainingTime == 0) {
                completed++;
                shortest.turnaroundTime = time - shortest.arrivalTime;
                shortest.waitingTime = shortest.turnaroundTime - shortest.burstTime;
            }
        }

        // Close last segment
        if (lastPID != null)
            gantt.add(new Segment(lastPID, segmentStart, time));

        // ===========================
        // OUTPUT RESULTS
        // ===========================
        System.out.println("\n===== SJF Preemptive (SRTF) Scheduling Result =====");
        System.out.println("PID\tAT\tBT\tWT\tTT");

        for (SJFProcess p : processes) {
            System.out.println(
                p.pid + "\t" + p.arrivalTime + "\t" + p.burstTime +
                "\t" + p.waitingTime + "\t" + p.turnaroundTime
            );
        }

        // ===========================
        // PRINT GANTT CHART
        // ===========================
        System.out.println("\n===== GANTT CHART =====");

        System.out.print("   ");
        for (Segment s : gantt)
            System.out.print("P" + s.pid + "     ");
        System.out.println();

        for (Segment s : gantt)
            System.out.print(s.start + "------");
        System.out.println(time);

        sc.close();
    }
}
