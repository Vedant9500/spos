import java.util.*;

class RRProcess {
    int pid, arrivalTime, burstTime;
    int remainingTime;
    int waitingTime, turnaroundTime;

    RRProcess(int pid, int at, int bt) {
        this.pid = pid;
        this.arrivalTime = at;
        this.burstTime = bt;
        this.remainingTime = bt;
    }
}

public class RoundRobinChart {

    static class GanttEntry {
        int pid, start, end;
        GanttEntry(int pid, int start, int end) {
            this.pid = pid;
            this.start = start;
            this.end = end;
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        System.out.print("Enter Time Quantum: ");
        int quantum = sc.nextInt();

        List<RRProcess> processes = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            System.out.println("\nEnter details for Process " + (i + 1) + ":");

            System.out.print("Process ID: ");
            int pid = sc.nextInt();

            System.out.print("Arrival Time: ");
            int at = sc.nextInt();

            System.out.print("Burst Time: ");
            int bt = sc.nextInt();

            processes.add(new RRProcess(pid, at, bt));
        }

        // Sort by Arrival Time
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));

        Queue<RRProcess> q = new LinkedList<>();
        List<GanttEntry> gantt = new ArrayList<>();

        int time = 0, i = 0;

        // Add first arrived process
        q.add(processes.get(0));
        i = 1;
        time = processes.get(0).arrivalTime;

        while (!q.isEmpty()) {
            RRProcess p = q.poll();

            int start = time;
            int exec = Math.min(quantum, p.remainingTime);
            p.remainingTime -= exec;
            time += exec;

            gantt.add(new GanttEntry(p.pid, start, time));

            while (i < n && processes.get(i).arrivalTime <= time) {
                q.add(processes.get(i));
                i++;
            }

            if (p.remainingTime > 0) {
                q.add(p);
            } else {
                p.turnaroundTime = time - p.arrivalTime;
                p.waitingTime = p.turnaroundTime - p.burstTime;
            }
        }

        // Output results
        System.out.println("\n===== Round Robin Scheduling =====");
        System.out.println("PID\tAT\tBT\tWT\tTT");

        for (RRProcess p : processes) {
            System.out.println(
                p.pid + "\t" + p.arrivalTime + "\t" + p.burstTime +
                "\t" + p.waitingTime + "\t" + p.turnaroundTime
            );
        }

        // -------------------------
        //       GANTT CHART
        // -------------------------
        System.out.println("\n===== Gantt Chart =====");

        // Top bar
        System.out.print(" ");
        for (GanttEntry g : gantt) {
            for (int k = 0; k < (g.end - g.start); k++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Middle (process IDs)
        System.out.print("|");
        for (GanttEntry g : gantt) {
            for (int k = 0; k < (g.end - g.start) - 1; k++)
                System.out.print(" ");
            System.out.print("P" + g.pid);
            for (int k = 0; k < (g.end - g.start) - 1; k++)
                System.out.print(" ");
            System.out.print("|");
        }
        System.out.println();

        // Bottom bar
        System.out.print(" ");
        for (GanttEntry g : gantt) {
            for (int k = 0; k < (g.end - g.start); k++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Timeline
        System.out.print(gantt.get(0).start);
        for (GanttEntry g : gantt) {
            for (int k = 0; k < (g.end - g.start); k++)
                System.out.print("  ");
            System.out.print(g.end);
        }

        sc.close();
    }
}
