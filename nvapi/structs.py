from ctypes import *
from .defines import *

class NvidiaThermalSensor(Structure):
	_fields_ = [
		("controller", c_int), # enum
		("defaultMinTemp", c_int32),
		("defaultMaxTemp", c_int32),
		("currentTemp", c_int32),
		("target", c_int), # enum
	]

class NvidiaThermalSettings(Structure):
	_fields_ = [
		("version", c_uint32),
		("count", c_uint32),
		("sensors", NvidiaThermalSensor * NVAPI_MAX_THERMAL_SENSORS_PER_GPU),
	]

class NvidiaMemoryInfo(Structure):
	_fields_ = [
		("version", c_uint32),
		("dedicatedVideoMemory", c_uint32),
		("availableDedicatedVideoMemory", c_uint32),
		("systemVideoMemory", c_uint32),
		("sharedSystemMemory", c_uint32),
		("curAvailableDedicatedVideoMemory", c_uint32),
		("dedicatedVideoMemoryEvictionsSize", c_uint32),
		("dedicatedVideoMemoryEvictionCount", c_uint32)
	]