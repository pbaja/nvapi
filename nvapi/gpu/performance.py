import ctypes
from ..enums import NvidiaPerfDecreaseReason, NvidiaClockFrequencyType
from nvapi.structs.performance import NvidiaPerfStatesInfo, NvidiaClockFrequencies

# See: https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpupstate.html

class GPUPerformanceSettings:
    '''Wrapper class for getting and setting performance gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu

    def perf_state(self) -> int:
        '''Returns current GPU performance level from 0 (maximum performance) to 12 (minimum idle power consumption)'''
        state = ctypes.c_int32()
        self._gpu.native.GPU_GetCurrentPstate(self._gpu.handle, ctypes.byref(state))
        return state.value

    def dynamic_perf_state_info(self):
        raise NotImplementedError() # GPU_GetDynamicPstatesInfoEx

    def perf_states_info(self) -> NvidiaPerfStatesInfo:
        struct = NvidiaPerfStatesInfo()
        struct.version = ctypes.sizeof(NvidiaPerfStatesInfo) | (2 << 16) #V2
        self._gpu.native.GPU_GetPstates20(self._gpu.handle, ctypes.byref(struct))
        return struct

    def enable_dynamic_perf_states(self, enabled):
        '''If set to false, prevents GPU from changing Pstate'''
        self._gpu.native.GPU_EnableDynamicPstates(self._gpu.handle, 0 if enabled else 1)

    def set_perf_states(self, struct):
        self._gpu.native.GPU_SetPstates20(self._gpu.handle, ctypes.byref(struct))

    def perf_decrease_info(self) -> NvidiaPerfDecreaseReason:
        info = ctypes.c_uint32()
        self._gpu.native.GPU_GetPerfDecreaseInfo(self._gpu.handle, ctypes.byref(info))
        return NvidiaPerfDecreaseReason(info.value)

    def all_clock_frequencies(self, clockType=None) -> NvidiaClockFrequencies:
        struct = NvidiaClockFrequencies()
        struct.version = ctypes.sizeof(NvidiaClockFrequencies) | (2 << 16) #V2
        struct.clockType = NvidiaClockFrequencyType.CURRENT_FREQ if clockType is None else clockType
        self._gpu.native.GPU_GetAllClockFrequencies(self._gpu.handle, ctypes.byref(struct))
        return struct