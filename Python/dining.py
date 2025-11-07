import threading
import time
import random

NUM_PHILOSOPHERS = 5

# Forks as mutexes
forks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]

def philosopher(phil_id):
    left_fork = forks[phil_id]
    right_fork = forks[(phil_id + 1) % NUM_PHILOSOPHERS]

    for _ in range(3):  # Each philosopher eats 3 times
        # Thinking
        print(f"Philosopher {phil_id} is thinking.")
        time.sleep(random.random())

        # Pick up forks
        # To avoid deadlock, odd philosophers pick left then right, even pick right then left
        if phil_id % 2 == 0:
            right_fork.acquire()
            left_fork.acquire()
        else:
            left_fork.acquire()
            right_fork.acquire()

        # Eating
        print(f"Philosopher {phil_id} is eating.")
        time.sleep(random.random())

        # Put down forks
        left_fork.release()
        right_fork.release()

# Create philosopher threads
philosophers = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM_PHILOSOPHERS)]

# Start threads
for p in philosophers:
    p.start()

# Wait for all threads to finish
for p in philosophers:
    p.join()

print("All philosophers have finished eating.")
