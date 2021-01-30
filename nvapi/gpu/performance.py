import ctypes
from ..enums import NvidiaPerfDecreaseReason, NvidiaClockFrequencyType
from nvapi.structs.performance import NvidiaPerfStatesInfo, NvidiaClockFrequencies

# See: https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpupstate.html

class GPUPerformanceSettings:
    '''Wrapper class for getting and setting performance gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu

    def getPerfState(self) -> int:
        '''Returns current GPU performance level from 0 (maximum performance) to 12 (minimum idle power consumption)'''
        state = ctypes.c_int32()
        self._gpu.native.GPU_GetCurrentPstate(self._gpu.handle, ctypes.byref(state))
        return state.value

    def getDynamicPerfStateInfo(self):
        raise NotImplementedError() # GPU_GetDynamicPstatesInfoEx

    def getPerfStates(self) -> NvidiaPerfStatesInfo:
        struct = NvidiaPerfStatesInfo()
        struct.version = ctypes.sizeof(NvidiaPerfStatesInfo) | (2 << 16) #V2
        self._gpu.native.GPU_GetPstates20(self._gpu.handle, ctypes.byref(struct))
        return struct

    def enableDynamicPstates(self, enabled):
        self._gpu.native.GPU_EnableDynamicPstates(self._gpu.handle, 0 if enabled else 1)

    def setPerfStates(self, struct):
        self._gpu.native.GPU_SetPstates20(self._gpu.handle, ctypes.byref(struct))

    def getPerfDecreaseInfo(self) -> NvidiaPerfDecreaseReason:
        info = ctypes.c_uint32()
        self._gpu.native.GPU_GetPerfDecreaseInfo(self._gpu.handle, ctypes.byref(info))
        return NvidiaPerfDecreaseReason(info.value)

    def getAllClockFrequencies(self, clockType=None):
        struct = NvidiaClockFrequencies()
        struct.version = ctypes.sizeof(NvidiaClockFrequencies) | (2 << 16) #V2
        struct.clockType = NvidiaClockFrequencyType.CURRENT_FREQ if clockType is None else clockType
        self._gpu.native.GPU_GetAllClockFrequencies(self._gpu.handle, ctypes.byref(struct))
        return struct