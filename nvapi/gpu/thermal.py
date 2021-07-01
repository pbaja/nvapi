import ctypes
from ..enums import NvidiaThermalTarget
from nvapi.structs.thermal import NvidiaThermalSettings


class GPUThermalSettings:
    '''Wrapper class for getting and setting thermal gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu

    def thermal_settings(self, sensorIdx=None):
        # Get info
        struct = NvidiaThermalSettings()
        struct.version = ctypes.sizeof(NvidiaThermalSettings) | (2 << 16) #V2
        if sensorIdx is None: sensorIdx = NvidiaThermalTarget.ALL
        self._gpu.native.GPU_GetThermalSettings(self._gpu.handle, sensorIdx, ctypes.byref(struct))
        return struct