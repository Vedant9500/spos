
import java.util.concurrent.Semaphore;
public class Semaphore1 {
    // ================= PRODUCER–CONSUMER PROBLEM =================
    static class SharedBuffer {
        int item;  // Shared data between producer and consumer

        // Semaphores for synchronization
        Semaphore mutex = new Semaphore(1);   // Ensures mutual exclusion
        Semaphore empty = new Semaphore(1);   // Buffer starts empty
        Semaphore full = new Semaphore(0);    // Buffer starts not full

        // Producer method
        public void produce(int value) throws InterruptedException {
            empty.acquire();   // Wait if buffer is full
            mutex.acquire();   // Lock the critical section
            item = value;
            System.out.println("Producer produced: " + item);
            mutex.release();   // Unlock critical section
            full.release();    // Signal that buffer has data
        }

        // Consumer method
        public void consume() throws InterruptedException {
            full.acquire();    // Wait if buffer is empty
            mutex.acquire();   // Lock the critical section

            System.out.println("Consumer consumed: " + item);

            mutex.release();   // Unlock critical section
            empty.release();   // Signal that buffer is empty
        }
    }

    // Producer thread
    static class Producer extends Thread {
        SharedBuffer buffer;
        Producer(SharedBuffer b) { buffer = b; }

        public void run() {
            for (int i = 1; i <= 5; i++) {
                try {
                    buffer.produce(i);
                    Thread.sleep(1000); // Simulate production time
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // Consumer thread
    static class Consumer extends Thread {
        SharedBuffer buffer;
        Consumer(SharedBuffer b) { buffer = b; }

        public void run() {
            for (int i = 1; i <= 5; i++) {
                try {
                    buffer.consume();
                    Thread.sleep(1500); // Simulate consumption time
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // ================= DINING PHILOSOPHERS PROBLEM =================
    static class DiningPhilosophers {
        static Semaphore[] forks = new Semaphore[5]; // One semaphore per fork
        static Semaphore mutex = new Semaphore(1);   // To avoid deadlock

        // Initialize forks
        static {
            for (int i = 0; i < 5; i++) {
                forks[i] = new Semaphore(1);
            }
        }

        // Philosopher thread
        static class Philosopher extends Thread {
            int id;
            Philosopher(int id) { this.id = id; }

            public void run() {
                try {
                    for (int i = 0; i < 3; i++) {
                        System.out.println("Philosopher " + id + " is thinking.");
                        Thread.sleep((int)(Math.random() * 1000));

                        // Acquire mutex before picking forks (avoid deadlock)
                        mutex.acquire();
                        forks[id].acquire();                // Pick left fork
                        forks[(id + 1) % 5].acquire();      // Pick right fork
                        mutex.release();

                        System.out.println("Philosopher " + id + " is eating.");
                        Thread.sleep((int)(Math.random() * 1000));

                        // Release both forks after eating
                        forks[id].release();
                        forks[(id + 1) % 5].release();

                        System.out.println("Philosopher " + id + " finished eating.");
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        // Start all philosopher threads
        public static Philosopher[] startDining() {
            Philosopher[] philosophers = new Philosopher[5];
            for (int i = 0; i < 5; i++) {
                philosophers[i] = new Philosopher(i);
                philosophers[i].start();
            }
            return philosophers;
        }
    }

    // ================= MAIN METHOD =================
    public static void main(String[] args) {
        // --- Producer–Consumer Problem Execution ---
        System.out.println("=== PRODUCER–CONSUMER PROBLEM ===");
        SharedBuffer buffer = new SharedBuffer();
        Producer producer = new Producer(buffer);
        Consumer consumer = new Consumer(buffer);


        producer.start();
        consumer.start();

        try {
            producer.join();
            consumer.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // --- Dining Philosophers Problem Execution ---
        System.out.println("\n=== DINING PHILOSOPHERS PROBLEM ===");
        DiningPhilosophers.Philosopher[] philosophers = DiningPhilosophers.startDining();

        // Wait for all philosophers to finish
        for (DiningPhilosophers.Philosopher p : philosophers) {
            try {
                p.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
