import ctypes
from ..structs import NvidiaMemoryInfo

class GPUDriverSettings:
    '''Wrapper class for getting and setting driver gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu

    def getMemoryInfo(self):
        # Get info
        struct = NvidiaMemoryInfo()
        struct.version = ctypes.sizeof(NvidiaMemoryInfo) | (3 << 16) #V3
        self._gpu.native.GPU_GetMemoryInfo(self._gpu.handle, ctypes.byref(struct))
        return struct