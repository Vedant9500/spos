import threading
import time
import random

NUM_PHILOSOPHERS = 5

# Semaphore for each fork
forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

# Semaphore to limit number of philosophers trying to pick forks simultaneously
# This prevents deadlock
room = threading.Semaphore(NUM_PHILOSOPHERS - 1)

def philosopher(phil_id):
    left_fork = forks[phil_id]
    right_fork = forks[(phil_id + 1) % NUM_PHILOSOPHERS]

    for _ in range(3):  # Each philosopher eats 3 times
        print(f"Philosopher {phil_id} is thinking.")
        time.sleep(random.random())

        room.acquire()  # Limit philosophers entering to avoid deadlock
        left_fork.acquire()
        right_fork.acquire()

        # Eating
        print(f"Philosopher {phil_id} is eating.")
        time.sleep(random.random())

        left_fork.release()
        right_fork.release()
        room.release()  # Philosopher leaves the table

# Create philosopher threads
philosophers = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM_PHILOSOPHERS)]

# Start threads
for p in philosophers:
    p.start()

# Wait for all threads to finish
for p in philosophers:
    p.join()

print("All philosophers have finished eating.")
