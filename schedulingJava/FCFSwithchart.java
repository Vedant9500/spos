import java.util.*;

class Process {
    int pid, arrivalTime, burstTime, waitingTime, turnaroundTime, startTime, endTime;

    Process(int pid, int at, int bt) {
        this.pid = pid;
        this.arrivalTime = at;
        this.burstTime = bt;
    }
}

public class FCFSwithchart {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        List<Process> processes = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            System.out.println("\nEnter details for Process " + (i + 1) + ":");

            System.out.print("Process ID: ");
            int pid = sc.nextInt();

            System.out.print("Arrival Time: ");
            int at = sc.nextInt();

            System.out.print("Burst/Service Time: ");
            int bt = sc.nextInt();

            processes.add(new Process(pid, at, bt));
        }

        // Sort by Arrival Time (FCFS)
        processes.sort(Comparator.comparingInt(p -> p.arrivalTime));

        int time = 0;

        for (Process p : processes) {
            time = Math.max(time, p.arrivalTime);

            p.startTime = time;
            p.waitingTime = time - p.arrivalTime;

            time += p.burstTime;
            p.endTime = time;

            p.turnaroundTime = p.waitingTime + p.burstTime;
        }

        System.out.println("\n===== FCFS Scheduling Result =====");
        System.out.println("PID\tAT\tBT\tST\tCT\tWT\tTT");

        for (Process p : processes) {
            System.out.println(p.pid + "\t" + p.arrivalTime + "\t" + p.burstTime +
                               "\t" + p.startTime + "\t" + p.endTime + "\t" +
                               p.waitingTime + "\t" + p.turnaroundTime);
        }

        // -------------------------
        //       GANTT CHART
        // -------------------------
        System.out.println("\n===== Gantt Chart =====");

        // Top bar
        System.out.print(" ");
        for (Process p : processes) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Process ID bar
        System.out.print("|");
        for (Process p : processes) {
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
        for (Process p : processes) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("--");
            System.out.print(" ");
        }
        System.out.println();

        // Timeline
        System.out.print("0");
        for (Process p : processes) {
            for (int i = 0; i < p.burstTime; i++)
                System.out.print("  ");
            System.out.print(p.endTime);
        }

        sc.close();
    }
}
