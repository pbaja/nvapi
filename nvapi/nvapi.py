import ctypes
from _ctypes import CFuncPtr

from .gpu import PhysicalGPU
from .constants import *
from .enums import *
from .structs import *


class NvidiaError(Exception):
    def __init__(self, msg, status):
        super().__init__(msg)
        self.status = status

class NvidiaFuncPtr(CFuncPtr):
    _flags_ = ctypes._FUNCFLAG_CDECL
    _restype_ = ctypes.c_int

class NvidiaNativeAPI:

    def __init__(self):

        # Load DLL
        try:
            self.api = ctypes.cdll.LoadLibrary('nvapi.dll')
        except: 
            try:
                self.api = ctypes.cdll.LoadLibrary('nvapi64.dll')
            except Exception as e:
                raise NvidiaError(f"Failed to load nvapi.dll: {e}")

        # Functions
        self.GetErrorMessage           = self._wrap(0x6C2D048C, raiseErrors=False)
        self.Initialize                = self._wrap(0x0150E828)
        self.GPU_GetFullName           = self._wrap(0xCEEE8E9F)
        self.GetInterfaceVersionString = self._wrap(0x01053FA5)
        self.EnumPhysicalGPUs          = self._wrap(0xE5AC921F)
        self.GPU_GetPstates20          = self._wrap(0x6FF81213)
        self.GPU_GetThermalSettings    = self._wrap(0xE3640A56)
        self.GPU_GetCurrentPstate      = self._wrap(0x927DA4F6)
        self.GPU_GetTachReading        = self._wrap(0x5F608315)

    def _wrap(self, address, raiseErrors=True):

        # Get function from pointer
        pointer = self.api.nvapi_QueryInterface(address)
        native_function = NvidiaFuncPtr(pointer)

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

    def __init__(self, verbose=False):
        self.native = NvidiaNativeAPI()

    def init(self):
        # Try to initialize
        self.native.Initialize()

        # Confirm interface version
        buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
        self.native.GetInterfaceVersionString(buf)
        self.version = buf.value.decode()
        if self.version != 'NVidia Complete Version 1.10':
            raise NvidiaError(f'Untested library version: {self.version}')

    def dispose(self):
        self.native.Unload()

    def getInterfaceVersion(self):
        return self.version

    def getDriverVersion(self):
        buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
        ver = ctypes.c_uint32()
        self.native.SYS_GetDriverAndBranchVersion(ctypes.byref(ver), buf)
        return {'driver': ver.value / 100.0, 'branch': buf.value.decode()}

    def getPhysicalGPUs(self):
        handles = (ctypes.c_void_p * NVAPI_MAX_PHYSICAL_GPUS)()
        count = ctypes.c_uint32()
        self.native.EnumPhysicalGPUs(ctypes.byref(handles), ctypes.byref(count))
        return [PhysicalGPU(handle, self.native) for handle in handles[:count.value]]