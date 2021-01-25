import ctypes
from .defines import *
from .structs import *
from .enums import *

class PhysicalGPU:

	def __init__(self, handle, native):
		self.handle = handle
		self.native = native

# GPU Info

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

# Thermal

	def getThermalSensors(self, sensorIdx=0):
		# Grab
		struct = NvidiaThermalSettings()
		struct.version = ctypes.sizeof(NvidiaThermalSettings) | (2 << 16)
		self.native.GPU_GetThermalSettings(self.handle, sensorIdx, ctypes.byref(struct))

		# Parse
		sensors = []
		for i in range(struct.count):
			sensor = struct.sensors[i]
			sensors.append({
				'controller': NvidiaThermalController(sensor.controller),
				'defaultMinTemp': sensor.defaultMinTemp,
				'defaultMaxTemp': sensor.defaultMaxTemp,
				'currentTemp': sensor.currentTemp,
				'target': NvidiaThermalTarget(sensor.target),
				})
		return sensors


