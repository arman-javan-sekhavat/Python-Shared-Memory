#************************* Writer Class *************************
#****************************************************************

import ctypes
import numpy as np
from multiprocessing import shared_memory


class Writer:
    kernel32 = ctypes.windll.kernel32

    def __init__(self, shape, dtype, shm_name, event1_name, event2_name):
        temp = np.zeros(shape, dtype)
        self.event1_name = event1_name
        self.event2_name = event2_name
        self.size = temp.nbytes
        self.shm = shared_memory.SharedMemory(name=shm_name, create=True, size=self.size)
        self.shared_arr = np.ndarray(shape=shape, dtype=dtype, buffer=self.shm.buf)
        self.event2 = self.kernel32.CreateEventA(None, False, False, bytes("Global\\" + self.event2_name, "ascii"))
        self.kernel32.WaitForSingleObject(self.event2, -1)
        self.event1 = self.kernel32.OpenEventA(0x0002, False, bytes("Global\\" + event1_name, "ascii"))

    def write(self, array):
        self.kernel32.WaitForSingleObject(self.event2, -1)
        self.shared_arr[:] = array[:]

    def done(self):
        self.kernel32.ResetEvent(self.event2)
        self.kernel32.SetEvent(self.event1)

    def disconnect(self):
        self.kernel32.CloseHandle(self.event1)
        self.kernel32.CloseHandle(self.event2)
        self.shm.close()
        self.shm.unlink()


#****************************************************************

writer = Writer((10, 10), np.float32, "SharedMemoryBlock", "SyncEvent1", "SyncEvent2")

for i in range(5):
    arr = np.random.uniform(low=-1.0, high=+1.0, size=(10, 10))
    
    writer.write(arr)
    print(arr)
    writer.done()

writer.disconnect()