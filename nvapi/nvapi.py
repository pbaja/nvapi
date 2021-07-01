import ctypes
from _ctypes import CFuncPtr
from typing import List

from .gpu import PhysicalGPU
from .constants import *
from .enums import *
from .structs import *


class NvidiaError(Exception):
    def __init__(self, msg, status):
        super().__init__(msg)
        self.status = status


class ApiError(Exception):
    pass


class NvidiaFuncPtr(CFuncPtr):
    _flags_ = ctypes._FUNCFLAG_CDECL
    _restype_ = ctypes.c_int


class NvidiaNativeAPI:

    def __init__(self):

        # Load DLL
        try:
            self.api = ctypes.cdll.LoadLibrary('nvapi64.dll')
        except: 
            try:
                self.api = ctypes.cdll.LoadLibrary('nvapi.dll')
            except Exception as e:
                raise ApiError(f"Failed to load nvapi.dll: {e}")

        # Functions
        self.GetErrorMessage                = self._wrap(0x6C2D048C, raiseErrors=False)
        self.Initialize                     = self._wrap(0x0150E828)
        self.Unload                         = self._wrap(0xD22BDD7E)
        self.GPU_GetFullName                = self._wrap(0xCEEE8E9F)
        self.GetInterfaceVersionString      = self._wrap(0x01053FA5)
        self.EnumPhysicalGPUs               = self._wrap(0xE5AC921F)
        self.GPU_GetPstates20               = self._wrap(0x6FF81213)
        self.GPU_SetPstates20               = self._wrap(0x0F4DAE6B)
        self.GPU_GetThermalSettings         = self._wrap(0xE3640A56)
        self.GPU_GetCurrentPstate           = self._wrap(0x927DA4F6)
        self.GPU_GetTachReading             = self._wrap(0x5F608315) # Up to GTX 1XXX
        self.GPU_GetCurrentFanSpeedLevel    = self._wrap(0xBD71F0C9) # Not supported
        self.GPU_GetMemoryInfo              = self._wrap(0x07F9B368)
        self.GPU_GetAllClockFrequencies     = self._wrap(0xDCB616C3)
        self.GPU_EnableDynamicPstates       = self._wrap(0xFA579A0F)
        self.GPU_GetCoolerSettings          = self._wrap(0xDA141340)
        self.GPU_GetGpuCoreCount            = self._wrap(0xC7026A87)
        self.GPU_GetVbiosVersionString      = self._wrap(0xA561FD7D)
        self.GPU_GetVbiosRevision           = self._wrap(0xACC3DA0A)
        self.GPU_GetVbiosOEMRevision        = self._wrap(0x2D43FB31)
        self.GPU_GetBusId                   = self._wrap(0x1BE0B8E5)
        self.GPU_GetBusSlotId               = self._wrap(0x2A0A350F)

        self.GPU_ClientFanCoolersGetInfo    = self._wrap(0xFB85B01E)
        self.GPU_ClientFanCoolersGetStatus  = self._wrap(0x35AED5E8)
        self.GPU_ClientFanCoolersGetControl = self._wrap(0x814B209F)
        self.GPU_ClientFanCoolersSetControl = self._wrap(0xA58971A5)

    def _wrap(self, address, raiseErrors=True):

        # Access violation workaround
        # THIS IS BAD. 
        # TOOD: Explore more. Test with more devices. Find out what is happening.
        paddr = self.api.nvapi_QueryInterface(0x0150E828)
        faddr = ctypes.cast(self.api.nvapi_QueryInterface, ctypes.c_void_p).value
        offset = (faddr-paddr) & 0xFFFF00000000

        # Get function from pointer
        pointer = self.api.nvapi_QueryInterface(address)
        native_function = NvidiaFuncPtr(pointer + offset)

        # Just return native function if we do not want to catch errors
        if not raiseErrors:
            return native_function

        # Catch errors and raise them as exceptions
        def wrapper(*args, **kwargs):
            # Execute
            result = native_function(*args, **kwargs)
            if result != NvidiaStatus.OK:
                msg = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
                self.GetErrorMessage(result, ctypes.byref(msg))
                raise NvidiaError(msg.value.decode(), NvidiaStatus(result))
            return None
        return wrapper

class NvidiaAPI:

    def __init__(self, initialize=True):
        self.native = NvidiaNativeAPI()
        self.initialize()

    def initialize(self):
        """Initializes Nvidia API. Must be called before all other functions. Can throw NvidiaError or ApiError, returns nothing."""

        # Try to initialize native API
        self.native.Initialize()

        # Confirm interface version
        buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
        self.native.GetInterfaceVersionString(buf)
        self.version = buf.value.decode()
        if self.version != 'NVidia Complete Version 1.10':
            raise ApiError(f'Untested library version: {self.version}')

    def dispose(self):
        """Disposes Nvidia API."""
        self.native.Unload()

    def interface_version(self):
        """Returns nvapi version"""
        return self.version

    def driver_version(self):
        """Returns dictionary with driver version"""
        buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
        ver = ctypes.c_uint32()
        self.native.SYS_GetDriverAndBranchVersion(ctypes.byref(ver), buf)
        return {'driver': ver.value / 100.0, 'branch': buf.value.decode()}

    def list_gpus(self) -> List[PhysicalGPU]:
        """Lists all installed Nvidia GPUs in the system"""
        handles = (ctypes.c_void_p * NVAPI_MAX_PHYSICAL_GPUS)()
        count = ctypes.c_uint32()
        self.native.EnumPhysicalGPUs(ctypes.byref(handles), ctypes.byref(count))
        return [PhysicalGPU(handle, self.native) for handle in handles[:count.value]]