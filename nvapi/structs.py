from ctypes import *
from .defines import *

NvS32 = c_int32

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

class NvidiaParamDelta(Structure):
	_fields_ = [
		("value", c_int32),
		("min", c_int32), # <- struct?
		("max", c_int32), # <^
	]

class NvidiaBaseVoltageEntry(Structure): # NV_GPU_PSTATE20_BASE_VOLTAGE_ENTRY_V1
	_fields_ = [
		("domainId", c_int32), # enum
		("blsEditable", c_uint32, 1),
		("reserved", c_uint32, 31),
		("volt_uV", c_uint32),
		("voltDelta_uV", NvidiaParamDelta),
	]

class NvidiaClockEntryDataSingle(Structure):
	_fields_ = [
		("freq_kHz", c_uint32)
	]

class NvidiaClockEntryDataRange(Structure):
	_fields_ = [
		("minFreq_kHz", c_uint32),
		("maxFreq_kHz", c_uint32),
		("domainId", c_int32), # enum
		("minVoltage_uV", c_uint32),
		("maxVoltage_uV", c_uint32)
	]

class NvidiaClockEntryData(Union):
	_fields_ = [
		("single", NvidiaClockEntryDataSingle),
		("range", NvidiaClockEntryDataRange)
	]

class NvidiaClockEntry(Structure): # NV_GPU_PSTATE20_CLOCK_ENTRY_V1
	_fields_ = [
		("domainId", c_int32), # enum
		("typeId", c_int32), # enum
		("blsEditable", c_uint32, 1),
		("reserved", c_uint32, 31),
		("freqDelta_kHz", NvidiaParamDelta),
		("data", NvidiaClockEntryData),
	]

class NvidiaPerfState(Structure):
	_fields_ = [
		("pStateId", c_int32), # enum
		("blsEditable", c_uint32, 1),
		("reserved", c_uint32, 31),
		("clocks", NvidiaClockEntry * NVAPI_MAX_GPU_PSTATE20_CLOCKS),
		("baseVoltages", NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
	]

class NvidiaOverVoltage(Structure):
	_fields_ = [
		("numVoltages", c_uint32),
		("voltages", NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
	]

class NvidiaPerfStatesInfo(Structure): # _NV_GPU_PERF_PSTATES20_INFO_V2
	_fields_ = [
		("version", c_uint32),
		("blsEditable", c_uint32, 1),
		("reserved", c_uint32, 31),
		("numPstates", c_uint32),
		("numClocks", c_uint32),
		("numBaseVoltages", c_uint32),
		("pstates", NvidiaPerfState * NVAPI_MAX_GPU_PSTATE20_PSTATES),
		("ov", NvidiaOverVoltage * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
	]