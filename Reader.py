#************************* Reader Class *************************
#****************************************************************

import ctypes
import numpy as np
from multiprocessing import shared_memory


class Reader:
    kernel32 = ctypes.windll.kernel32

    def __init__(self, shape, dtype, shm_name, event1_name, event2_name):
        temp = np.zeros(shape, dtype)
        self.event1_name = event1_name
        self.event2_name = event2_name
        self.size = temp.nbytes
        self.shm = shared_memory.SharedMemory(name=shm_name, create=False)
        self.shared_arr = np.ndarray(shape=shape, dtype=dtype, buffer=self.shm.buf)
        self.event1 = self.kernel32.CreateEventA(None, False, False, bytes("Global\\" + self.event1_name, "ascii"))
        self.event2 = self.kernel32.OpenEventA(0x0002, False, bytes("Global\\" + event2_name, "ascii"))
        self.kernel32.SetEvent(self.event2)
        self.kernel32.SetEvent(self.event2)

    def read(self):
        self.kernel32.WaitForSingleObject(self.event1, -1)
        return self.shared_arr.copy()
    
    def done(self):
        self.kernel32.ResetEvent(self.event1)
        self.kernel32.SetEvent(self.event2)

    def disconnect(self):
        self.kernel32.CloseHandle(self.event1)
        self.kernel32.CloseHandle(self.event2)
        self.shm.close()


#****************************************************************

reader = Reader((10, 10), np.float32, "SharedMemoryBlock", "SyncEvent1", "SyncEvent2")

for i in range(5):
    arr = reader.read()
    print(arr)
    reader.done()

reader.disconnect()