import ctypes
from .defines import *
from .structs import *
from .enums import *

class PhysicalGPU:

	def __init__(self, handle, native):
		self.handle = handle
		self.native = native

# General https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpu.html

	def getFullName(self):
		name = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		self.native.GPU_GetFullName(self.handle, name)
		return name.value.decode()

	def getCoreCount(self):
		count = ctypes.c_uint32()
		self.native.GPU_GetGpuCoreCount(self.handle, ctypes.byref(count))
		return count.value

	def getBiosVersion(self):
		version = ctypes.create_string_buffer(NVAPI_SHORT_STRING_MAX)
		self.native.GPU_GetVbiosVersionString(self.handle, version)
		return version.value.decode()

	def getBiosRevision(self):
		revision = ctypes.c_uint32()
		self.native.GPU_GetVbiosRevision(self.handle, ctypes.byref(revision))
		return revision.value

	def getBiosOEMRevision(self):
		revision = ctypes.c_uint32()
		self.native.GPU_GetVbiosOEMRevision(self.handle, ctypes.byref(revision))
		return revision.value

	def getBusId(self):
		busid = ctypes.c_uint32()
		self.native.GPU_GetBusId(self.handle, ctypes.byref(busid))
		return busid.value

	def getBusSlotId(self):
		slotid = ctypes.c_uint32()
		self.native.GPU_GetBusSlotId(self.handle, ctypes.byref(slotid))
		return slotid.value

# Performance https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpuPerf.html

	def getPerfDecreaseInfo(self):
		info = ctypes.c_uint32()
		self.native.GPU_GetPerfDecreaseInfo(self.handle, ctypes.byref(info))
		return NvidiaPerfDecreaseReason(info.value)

# Thermal https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gputhermal.html

	def getThermalSensors(self, sensorIdx=None):
		# Get info
		struct = NvidiaThermalSettings()
		struct.version = ctypes.sizeof(NvidiaThermalSettings) | (2 << 16) #V2
		if sensorIdx is None: sensorIdx = NvidiaThermalTarget.ALL
		self.native.GPU_GetThermalSettings(self.handle, sensorIdx, ctypes.byref(struct))
		return struct

#
# Performance State https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpupstate.html
# P0/P1 - Maximum 3D performance
# P2/P3 - Balanced 3D performance-power
# P8 - Basic HD video playback
# P10 - DVD playback
# P12 - Minimum idle power consumption
#
	def getPerfState(self): # GPU_GetCurrentPstate
		state = ctypes.c_int32()
		self.native.GPU_GetCurrentPstate(self.handle, ctypes.byref(state))
		return NvidiaPerformanceState(state.value)

	def getDynamicPerfStateInfo(self):
		raise NotImplementedError() # GPU_GetDynamicPstatesInfoEx

	def getPerfStates(self):
		struct = NvidiaPerfStatesInfo()
		struct.version = ctypes.sizeof(NvidiaPerfStatesInfo) | (2 << 16) #V2
		self.native.GPU_GetPstates20(self.handle, ctypes.byref(struct))
		return struct

# Clock Control https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpuclock.html

	def getAllClockFrequencies(self):
		raise NotImplementedError() # GPU_GetAllClockFrequencies

# Cooler Interface https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__gpucooler.html

	def getTachReading(self):
		reading = ctypes.c_uint32()
		self.native.GPU_GetTachReading(self.handle, ctypes.byref(reading))
		return reading.value

# Graphics Driver https://docs.nvidia.com/gameworks/content/gameworkslibrary/coresdk/nvapi/group__driverapi.html

	def getMemoryInfo(self):
		# Get info
		struct = NvidiaMemoryInfo()
		struct.version = ctypes.sizeof(NvidiaMemoryInfo) | (3 << 16) #V3
		self.native.GPU_GetMemoryInfo(self.handle, ctypes.byref(struct))
		return struct