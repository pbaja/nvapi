import ctypes
from _ctypes import CFuncPtr

from . import functions, gpu
from .defines import *
from .enums import *
from .structs import *

class NvidiaError(Exception):
	pass


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
				return

		# Create functions
		for attr, addr in functions.address_map.items():
			# Get .dll function
			pointer = self.api.nvapi_QueryInterface(addr)
			function = NvidiaFuncPtr(pointer)
			function_wrapped = self._ErrorWrapper(function)

			# Add to object
			setattr(self, attr, function_wrapped)

	def _ErrorWrapper(self, function):
		def wrapper(*args, **kwargs):
			result = function(*args, **kwargs)
			if result != NvidiaStatus.OK:
				buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
				self.GetErrorMessage(result, buf)
				raise NvidiaError(buf.value.decode())
			return None
		return wrapper

	def GetErrorMessage(self, code):
		# See: https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__nvapistatus.html
		msg = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		self._GetErrorMessage(code, msg)
		return msg.value.decode()


class NvidiaAPI:

	def __init__(self, verbose=False):
		self.native = NvidiaNativeAPI()

	def init(self):
		# Try to initialize
		self.native.Initialize()

		# Check interface version
		buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		self.native.GetInterfaceVersionString(buf)
		self.version = buf.value.decode()
		if self.version != 'NVidia Complete Version 1.10':
			raise NvidiaError(f'Untested library version: {self.version}')

	def dispose(self):
		self.native.Unload()

	def interfaceVersion(self):
		#buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		#self.native.GetInterfaceVersionString(buf)
		#return buf.value.decode()
		return self.version

	def driverVersion(self):
		buf = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		ver = ctypes.c_uint32()
		self.native.SYS_GetDriverAndBranchVersion(ctypes.byref(ver), buf)
		return {'driver': ver.value / 100.0, 'branch': buf.value.decode()}

	def getPhysicalGPUs(self):
		handles = (ctypes.c_void_p * NVAPI_MAX_PHYSICAL_GPUS)()
		count = ctypes.c_uint32()
		self.native.EnumPhysicalGPUs(ctypes.byref(handles), ctypes.byref(count))
		return [gpu.PhysicalGPU(handle, self.native) for handle in handles[:count.value]]