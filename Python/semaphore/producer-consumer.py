import threading
import time
import random

# Shared buffer
BUFFER_SIZE = 5
buffer = []

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)  # Tracks empty slots
full = threading.Semaphore(0)             # Tracks filled slots
mutex = threading.Semaphore(1)            # Binary semaphore for mutual exclusion

NUM_ITEMS = 10  # Total items to produce/consume

# Producer function
def producer():
    global buffer
    for _ in range(NUM_ITEMS):
        item = random.randint(1, 100)
        empty.acquire()  # Wait if buffer is full
        mutex.acquire()  # Enter critical section
        buffer.append(item)
        print(f"Producer produced: {item}, Buffer: {buffer}")
        mutex.release()  # Exit critical section
        full.release()   # Signal that an item is available
        time.sleep(random.random())

# Consumer function
def consumer():
    global buffer
    for _ in range(NUM_ITEMS):
        full.acquire()   # Wait if buffer is empty
        mutex.acquire()  # Enter critical section
        item = buffer.pop(0)
        print(f"Consumer consumed: {item}, Buffer: {buffer}")
        mutex.release()  # Exit critical section
        empty.release()  # Signal that a slot is empty
        time.sleep(random.random())

# Create threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start threads
producer_thread.start()
consumer_thread.start()

# Wait for threads to finish
producer_thread.join()
consumer_thread.join()

print("All items produced and consumed.")
