import threading
import time
import random

# Shared data
data = 0

# Locks
read_count_lock = threading.Lock()  # Protects read_count
resource_lock = threading.Lock()    # Protects shared resource

read_count = 0  # Number of active readers

# Reader thread
def reader(reader_id):
    global read_count
    global data

    for _ in range(3):
        # Entry section
        read_count_lock.acquire()
        read_count += 1
        if read_count == 1:
            resource_lock.acquire()  # First reader locks resource
        read_count_lock.release()

        # Critical section (reading)
        print(f"Reader {reader_id} is reading data: {data}")
        time.sleep(random.random())  # Simulate read time

        # Exit section
        read_count_lock.acquire()
        read_count -= 1
        if read_count == 0:
            resource_lock.release()  # Last reader releases resource
        read_count_lock.release()

        time.sleep(random.random())

# Writer thread
def writer(writer_id):
    global data

    for _ in range(3):
        resource_lock.acquire()  # Exclusive access
        data += 1
        print(f"Writer {writer_id} is writing data: {data}")
        time.sleep(random.random())  # Simulate write time
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
