import ctypes
from ..constants import *

# See: https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpu.html

class GPUGeneralSettings:
    '''Wrapper class for getting and setting general gpu settings and information'''

    def __init__(self, gpu):
        self._gpu = gpu
        self._full_name = None 

    def full_name(self) -> str:
        '''Retrieves full gpu name as string - for example, "GeForce RTX3060Ti".'''
        if self._full_name is None:
            name = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
            self._gpu.native.GPU_GetFullName(self._gpu.handle, name)
            self._full_name = name.value.decode()
        return self._full_name

    def core_count(self) -> int:
        '''Total number of cores defined for a GPU.'''
        count = ctypes.c_uint32()
        self._gpu.native.GPU_GetGpuCoreCount(self._gpu.handle, ctypes.byref(count))
        return count.value

    def bios_version(self) -> str:
        '''Returns full video BIOS version string in the form of xx.xx.xx.xx.yy where xx numbers come from BiosRevision and yy from OEM revision.'''
        version = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
        self._gpu.native.GPU_GetVbiosVersionString(self._gpu.handle, version)
        return version.value.decode()

    def bios_revision(self) -> int:
        '''Returns the revision of the video BIOS'''
        revision = ctypes.c_uint32()
        self._gpu.native.GPU_GetVbiosRevision(self._gpu.handle, ctypes.byref(revision))
        return revision.value

    def bios_oem_revision(self) -> int:
        '''Returns the OEM revision of the video BIOS'''
        revision = ctypes.c_uint32()
        self._gpu.native.GPU_GetVbiosOEMRevision(self._gpu.handle, ctypes.byref(revision))
        return revision.value

    def bus_id(self) -> int:
        '''ID of the bus associated with this GPU'''
        busid = ctypes.c_uint32()
        self._gpu.native.GPU_GetBusId(self._gpu.handle, ctypes.byref(busid))
        return busid.value

    def bus_slot_id(self) -> int:
        '''ID of the bus slot associated with this GPU'''
        slotid = ctypes.c_uint32()
        self._gpu.native.GPU_GetBusSlotId(self._gpu.handle, ctypes.byref(slotid))
        return slotid.value