import java.util.concurrent.locks.*;
import java.util.Random;

public class Dining {
    private static final Lock[] forks = new ReentrantLock[5];
    private static final Random rand = new Random();

    static class Philosopher extends Thread {
        int id;

        Philosopher(int id) { this.id = id; }

        private void think() throws InterruptedException {
            System.out.println("Philosopher " + id + " is THINKING");
            Thread.sleep(rand.nextInt(500) + 200);
        }

        private void eat() throws InterruptedException {
            System.out.println("Philosopher " + id + " is EATING");
            Thread.sleep(rand.nextInt(400) + 200);
        }

        public void run() {
            try {
                while (true) {
                    think();  // Thinking
                    
                    int left = id;
                    int right = (id + 1) % 5;

                    // Pick up both forks using mutex
                    forks[left].lock();
                    forks[right].lock();

                    eat();   // Eating

                    // Release forks
                    forks[left].unlock();
                    forks[right].unlock();

                    System.out.println("Philosopher " + id + " FINISHED EATING");
                }
            } catch (InterruptedException e) {
                // Stop thread when interrupted
            }
        }
    }

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < 5; i++)
            forks[i] = new ReentrantLock();

        Philosopher[] p = new Philosopher[5];

        for (int i = 0; i < 5; i++) {
            p[i] = new Philosopher(i);
            p[i].start();
        }

        // Let simulation run for 5 seconds
        Thread.sleep(5000);

        // Stop all philosophers
        for (int i = 0; i < 5; i++) p[i].interrupt();
        for (int i = 0; i < 5; i++) p[i].join();

        System.out.println("Simulation ended.");
    }
}
