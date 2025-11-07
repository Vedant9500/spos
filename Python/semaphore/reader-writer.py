import threading
import time
import random

# Shared data
data = 0

# Semaphores
read_count_lock = threading.Semaphore(1)  # Protects read_count
resource_lock = threading.Semaphore(1)    # Protects shared resource

read_count = 0  # Number of active readers

# Reader function
def reader(reader_id):
    global read_count, data
    for _ in range(3):
        read_count_lock.acquire()
        read_count += 1
        if read_count == 1:  # First reader locks resource
            resource_lock.acquire()
        read_count_lock.release()

        # Reading
        print(f"Reader {reader_id} is reading data: {data}")
        time.sleep(random.random())

        read_count_lock.acquire()
        read_count -= 1
        if read_count == 0:  # Last reader releases resource
            resource_lock.release()
        read_count_lock.release()
        time.sleep(random.random())

# Writer function
def writer(writer_id):
    global data
    for _ in range(3):
        resource_lock.acquire()  # Exclusive access
        data += 1
        print(f"Writer {writer_id} is writing data: {data}")
        time.sleep(random.random())
        resource_lock.release()
        time.sleep(random.random())

# Create threads
readers = [threading.Thread(target=reader, args=(i,)) for i in range(3)]
writers = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

# Start threads
for w in writers:
    w.start()
for r in readers:
    r.start()

# Wait for all threads to finish
for w in writers:
    w.join()
for r in readers:
    r.join()

print("All readers and writers have finished.")
