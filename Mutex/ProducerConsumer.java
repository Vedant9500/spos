import java.util.concurrent.locks.*;

public class ProducerConsumer {
    private static int buffer = 0;
    private static boolean empty = true;

    private static final Lock mutex = new ReentrantLock();
    private static final Condition condition = mutex.newCondition();

    static class Producer extends Thread {
        public void run() {
            for (int i = 1; i <= 5; i++) {
                mutex.lock();
                try {
                    while (!empty) condition.await();
                    buffer = i;
                    System.out.println("Produced: " + i);
                    empty = false;
                    condition.signalAll();
                } catch (Exception e) {} 
                finally { mutex.unlock(); }
            }
        }
    }

    static class Consumer extends Thread {
        public void run() {
            for (int i = 1; i <= 5; i++) {
                mutex.lock();
                try {
                    while (empty) condition.await();
                    System.out.println("Consumed: " + buffer);
                    empty = true;
                    condition.signalAll();
                } catch (Exception e) {} 
                finally { mutex.unlock(); }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Thread p = new Producer();
        Thread c = new Consumer();
        p.start(); c.start();
        p.join(); c.join();
    }
}
