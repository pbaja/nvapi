import ctypes
from nvapi.structs.cooler import NvidiaFanCoolersControl, NvidiaFanCoolersStatus, NvidiaCoolerSettings
from ..enums import NvidiaCoolerTarget

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
        if target is None: target = NvidiaCoolerTarget.ALL
        self._gpu.native.GPU_GetCoolerSettings(self._gpu.handle, target, ctypes.byref(struct))
        return struct

    def getClientFanCoolersStatus(self) -> NvidiaFanCoolersStatus:
        struct = NvidiaFanCoolersStatus()
        struct.version = ctypes.sizeof(NvidiaFanCoolersStatus) | (1 << 16) #V1
        self._gpu.native.GPU_ClientFanCoolersGetStatus(self._gpu.handle, ctypes.byref(struct))
        return struct

    def getClientFanCoolersControl(self) -> NvidiaFanCoolersControl:
        struct = NvidiaFanCoolersControl()
        struct.version = ctypes.sizeof(NvidiaFanCoolersControl) | (1 << 16) #V1
        self._gpu.native.GPU_ClientFanCoolersGetControl(self._gpu.handle, ctypes.byref(struct))
        return struct

    def setClientFanCoolersControl(self, struct:NvidiaFanCoolersControl):
        struct.version = ctypes.sizeof(NvidiaFanCoolersControl) | (1 << 16) #V1
        self._gpu.native.GPU_ClientFanCoolersSetControl(self._gpu.handle, ctypes.byref(struct))