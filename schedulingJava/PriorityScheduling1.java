import java.util.*;

class PSProcess {
    int pid, arrivalTime, burstTime, priority;
    int waitingTime, turnaroundTime, startTime, completionTime;

    PSProcess(int pid, int at, int bt, int pr) {
        this.pid = pid;
        this.arrivalTime = at;
        this.burstTime = bt;
        this.priority = pr;
    }
}

public class PriorityScheduling1 {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        List<PSProcess> processes = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            System.out.println("\nEnter details for Process " + (i + 1) + ":");

            System.out.print("Process ID: ");
            int pid = sc.nextInt();

            System.out.print("Arrival Time: ");
            int at = sc.nextInt();

            System.out.print("Burst Time: ");
            int bt = sc.nextInt();

            System.out.print("Priority (lower number = higher priority): ");
            int pr = sc.nextInt();

            processes.add(new PSProcess(pid, at, bt, pr));
        }

        // Sort by arrival time
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));

        int time = 0;
        List<PSProcess> completed = new ArrayList<>();

        // Non-preemptive Priority Scheduling
        while (completed.size() < processes.size()) {

            PSProcess highest = null;

            for (PSProcess p : processes) {
                if (!completed.contains(p) && p.arrivalTime <= time) {
                    if (highest == null || p.priority < highest.priority) {
                        highest = p;
                    }
                }
            }

            if (highest == null) {
                time++;
                continue;
            }

            highest.startTime = time;
            highest.waitingTime = time - highest.arrivalTime;

            time += highest.burstTime;
            highest.completionTime = time;

            highest.turnaroundTime = highest.completionTime - highest.arrivalTime;

            completed.add(highest);
        }

        System.out.println("\n===== Priority Scheduling (Non-Preemptive) =====");
        System.out.println("PID\tAT\tBT\tPR\tST\tCT\tWT\tTT");

        for (PSProcess p : processes) {
            System.out.println(
                p.pid + "\t" + p.arrivalTime + "\t" + p.burstTime + "\t" +
                p.priority + "\t" + p.startTime + "\t" + p.completionTime + "\t" +
                p.waitingTime + "\t" + p.turnaroundTime
            );
        }

        // -------------------------
        //       GANTT CHART
        // -------------------------
        System.out.println("\n===== Gantt Chart =====");

        // Top bar
        System.out.print(" ");
        for (PSProcess p : completed) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Middle bar with process IDs
        System.out.print("|");
        for (PSProcess p : completed) {
            for (int i = 0; i < p.burstTime - 1; i++)
                System.out.print(" ");
            System.out.print("P" + p.pid);
            for (int i = 0; i < p.burstTime - 1; i++)
                System.out.print(" ");
            System.out.print("|");
        }
        System.out.println();

        // Bottom bar
        System.out.print(" ");
        for (PSProcess p : completed) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Timeline
        System.out.print(processes.get(0).startTime);
        for (PSProcess p : completed) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("  ");
            System.out.print(p.completionTime);
        }

        sc.close();
    }
}
