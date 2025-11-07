import threading
import time
import random

# Shared buffer
buffer = []
BUFFER_SIZE = 5

# Mutex lock
mutex = threading.Lock()

# Semaphore-like variables for empty/full slots
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

def producer():
    global buffer
    while True:
        item = random.randint(1, 100)
        empty.acquire()  # Wait if buffer is full
        mutex.acquire()  # Enter critical section
        buffer.append(item)
        print(f"Producer produced: {item}, Buffer: {buffer}")
        mutex.release()  # Exit critical section
        full.release()  # Signal that an item is available
        time.sleep(random.random())

def consumer():
    global buffer
    while True:
        full.acquire()  # Wait if buffer is empty
        mutex.acquire()  # Enter critical section
        item = buffer.pop(0)
        print(f"Consumer consumed: {item}, Buffer: {buffer}")
        mutex.release()  # Exit critical section
        empty.release()  # Signal that space is available
        time.sleep(random.random())

# Creating threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()
