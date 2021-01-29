import ctypes
from ..enums import NvidiaCoolerTarget
from ..structs import NvidiaCoolerSettings

# See: https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpucooler.html

class GPUCoolerSettings:
    '''Wrapper class for getting and setting performance gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu

    def getTachReading(self) -> int:
        '''Returns current fan speed in RPM. Supported only up to GTX 1XXX.'''
        reading = ctypes.c_uint32()
        self._gpu.native.GPU_GetTachReading(self._gpu.handle, ctypes.byref(reading))
        return reading.value

    def getCoolerSettings(self, target:NvidiaCoolerTarget=None) -> NvidiaCoolerSettings:
        '''Returns structure with cooler settings for specified target. All targets will be retrieved if not specified.'''
        struct = NvidiaCoolerSettings()
        struct.version = ctypes.sizeof(NvidiaCoolerSettings) | (1 << 16) #V1
        if target is None: target = NvidiaCoolerTarget.All
        self._gpu.native.GPU_GetCoolerSettings(self._gpu.handle, target, ctypes.byref(struct))
        return struct