import threading
import time
import random

# ================= PRODUCER–CONSUMER PROBLEM =================
class SharedBuffer:
    def __init__(self):
        self.item = None  # Shared data between producer and consumer
        self.mutex = threading.Semaphore(1)  # Ensures mutual exclusion
        self.empty = threading.Semaphore(1)  # Buffer starts empty
        self.full = threading.Semaphore(0)   # Buffer starts not full

    def produce(self, value):
        self.empty.acquire()  # Wait if buffer is full
        self.mutex.acquire()  # Lock the critical section
        self.item = value
        print(f"Producer produced: {self.item}")
        self.mutex.release()  # Unlock critical section
        self.full.release()   # Signal that buffer has data

    def consume(self):
        self.full.acquire()   # Wait if buffer is empty
        self.mutex.acquire()  # Lock the critical section
        print(f"Consumer consumed: {self.item}")
        self.mutex.release()  # Unlock critical section
        self.empty.release()  # Signal that buffer is empty


class Producer(threading.Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        for i in range(1, 6):
            self.buffer.produce(i)
            time.sleep(1)  # Simulate production time


class Consumer(threading.Thread):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def run(self):
        for _ in range(1, 6):
            self.buffer.consume()
            time.sleep(1.5)  # Simulate consumption time


# ================= DINING PHILOSOPHERS PROBLEM =================
class DiningPhilosophers:
    forks = [threading.Semaphore(1) for _ in range(5)]  # One semaphore per fork
    mutex = threading.Semaphore(1)  # To avoid deadlock

    class Philosopher(threading.Thread):
        def __init__(self, id):
            super().__init__()
            self.id = id

        def run(self):
            for _ in range(3):  # Each philosopher eats 3 times
                print(f"Philosopher {self.id} is thinking.")
                time.sleep(random.uniform(0.5, 1.5))

                # Acquire mutex before picking forks to avoid deadlock
                DiningPhilosophers.mutex.acquire()
                DiningPhilosophers.forks[self.id].acquire()          # Pick left fork
                DiningPhilosophers.forks[(self.id + 1) % 5].acquire()  # Pick right fork
                DiningPhilosophers.mutex.release()

                print(f"Philosopher {self.id} is eating.")
                time.sleep(random.uniform(0.5, 1.5))

                # Release both forks
                DiningPhilosophers.forks[self.id].release()
                DiningPhilosophers.forks[(self.id + 1) % 5].release()

                print(f"Philosopher {self.id} finished eating.")

    @staticmethod
    def start_dining():
        philosophers = [DiningPhilosophers.Philosopher(i) for i in range(5)]
        for p in philosophers:
            p.start()
        return philosophers


# ================= MAIN METHOD =================
if __name__ == "__main__":
    # --- Producer–Consumer Problem Execution ---
    print("=== PRODUCER–CONSUMER PROBLEM ===")
    buffer = SharedBuffer()
    producer = Producer(buffer)
    consumer = Consumer(buffer)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    # --- Dining Philosophers Problem Execution ---
    print("\n=== DINING PHILOSOPHERS PROBLEM ===")
    philosophers = DiningPhilosophers.start_dining()

    # Wait for all philosophers to finish
    for p in philosophers:
        p.join()
