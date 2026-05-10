# Python-Shared-Memory
This repository provides a high-speed and reliable channel for communication between two separate Python interpreters.

## A Python Implementation of the Shared Memory, Synchronized by the Windows Kernel Functions

* This repository contains two Python scripts, Writer and Reader. These can be used to share data in the form of NumPy arrays between two separate Python interpreters on the same machine. This implementation focuses on maximizing the transfer speed and preventing information loss during the transfer, achieved by utilizing the Windows Kernel synchronization functions.

* The resulting communication channel consists of two nodes, the Writer and the Reader and is simplex (unidirectional). Each of these nodes is implemented in a separate Python interpreter. Two Python classes are designed, one for each of these nodes.

Note: The Writer script must be executed before the Reader script.

## Example Usage
```python
#------------------------------------- Writer node -------------------------------------

import PyWinSHM

# Creating the writer object
writer = PyWinSHM.Writer(shape=(10, 10), dtype=np.float32, shm_name="SharedMemoryBlock",
                          event1_name="SyncEvent1", event2_name="SyncEvent2")

# Data (Numpy arrays) to be transferred
data = np.array([[2.0, 3.0], [5.0, 7.0]])

for arr in data:
    writer.write(arr)
    print(arr)
    writer.done()

# Cleanup
writer.disconnect()
```

```python
#------------------------------------- Reader node -------------------------------------

import PyWinSHM

# Creating the reader object
reader = PyWinSHM.Reader(shape=(10, 10), dtype=np.float32, shm_name="SharedMemoryBlock",
                event1_name="SyncEvent1", event2_name="SyncEvent2")

for i in range(2):
    arr = reader.read()
    print(arr)
    reader.done()

# Cleanup
reader.disconnect()
```
