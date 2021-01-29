import ctypes
from ..enums import NvidiaPerfDecreaseReason
from ..structs import NvidiaPerfStatesInfo

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

    def getPerfDecreaseInfo(self) -> NvidiaPerfDecreaseReason:
        info = ctypes.c_uint32()
        self._gpu.native.GPU_GetPerfDecreaseInfo(self._gpu.handle, ctypes.byref(info))
        return NvidiaPerfDecreaseReason(info.value)