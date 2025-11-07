import java.util.concurrent.locks.*;

public class ReaderWriter {
    // Use a ReentrantReadWriteLock to coordinate readers and writers correctly.
    private static final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();

    static class Reader extends Thread {
        int id;
        Reader(int id) { this.id = id; }

        public void run() {
            rwLock.readLock().lock();
            try {
                System.out.println("Reader " + id + " is READING");
            } finally {
                rwLock.readLock().unlock();
            }
        }
    }

    static class Writer extends Thread {
        int id;
        Writer(int id) { this.id = id; }

        public void run() {
            rwLock.writeLock().lock();
            try {
                System.out.println("Writer " + id + " is WRITING");
            } finally {
                rwLock.writeLock().unlock();
            }
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