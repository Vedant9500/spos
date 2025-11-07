import java.util.concurrent.locks.*;

public class ReaderWriter {
    private static int readCount = 0;

    private static final Lock mutex = new ReentrantLock();     // For readCount
    private static final Lock writeLock = new ReentrantLock(); // For writers

    static class Reader extends Thread {
        int id;
        Reader(int id) { this.id = id; }

        public void run() {
            mutex.lock();
            readCount++;
            if (readCount == 1) writeLock.lock(); // First reader blocks writers
            mutex.unlock();

            System.out.println("Reader " + id + " is READING");

            mutex.lock();
            readCount--;
            if (readCount == 0) writeLock.unlock(); // Last reader unblocks writers
            mutex.unlock();
        }
    }

    static class Writer extends Thread {
        int id;
        Writer(int id) { this.id = id; }

        public void run() {
            writeLock.lock();
            System.out.println("Writer " + id + " is WRITING");
            writeLock.unlock();
        }
    }

    public static void main(String[] args) throws Exception {
        Thread r1 = new Reader(1);
        Thread r2 = new Reader(2);
        Thread w1 = new Writer(1);

        r1.start();
        r2.start();
        w1.start();

        r1.join(); r2.join(); w1.join();
    }
}
