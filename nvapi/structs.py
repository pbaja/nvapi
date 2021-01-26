from ctypes import *
from .defines import *

# Data types
c_enum = c_int32

def _getitem(self, i):
	name = self._fields_[i][0]
	value = getattr(self, name)
	if isinstance(value, Structure) or isinstance(value, Union):
		value = dict(value)
	return (name, value)

def struct(name, fields):
	StructType = type(name, (Structure,), { '_fields_': fields, '__getitem__': _getitem})
	globals()[name] = StructType
	return StructType

def union(name, structs):
	UnionType = type(name, (Union,), {'_fields_': structs, '__getitem__': _getitem })
	globals()[name] = UnionType
	return UnionType


struct('NvidiaThermalSettings', [
		("version", c_uint32),
		("count", c_uint32),

		("sensors", struct('NvidiaThermalSensor', [
			("controller", c_int), # enum
			("defaultMinTemp", c_int32),
			("defaultMaxTemp", c_int32),
			("currentTemp", c_int32),
			("target", c_enum),
		]) * NVAPI_MAX_THERMAL_SENSORS_PER_GPU)
	])

struct('NvidiaMemoryInfo', [
	("version", c_uint32),
	("dedicatedVideoMemory", c_uint32),
	("availableDedicatedVideoMemory", c_uint32),
	("systemVideoMemory", c_uint32),
	("sharedSystemMemory", c_uint32),
	("curAvailableDedicatedVideoMemory", c_uint32),
	("dedicatedVideoMemoryEvictionsSize", c_uint32),
	("dedicatedVideoMemoryEvictionCount", c_uint32)
])

struct('NvidiaParamDelta', [ # NV_GPU_PERF_PSTATES20_PARAM_DELTA
	("value", c_int32),
	("valueRange", struct('MinMax', [
		("min", c_int32),
		("max", c_int32)
	]))
])

struct('NvidiaBaseVoltageEntry', [ # NV_GPU_PSTATE20_BASE_VOLTAGE_ENTRY_V1 
	("domainId", c_enum),
	("blsEditable", c_uint32, 1),
	("reserved", c_uint32, 31),
	("volt_uV", c_uint32),
	("voltDelta_uV", NvidiaParamDelta),
])

struct('NvidiaClockEntry', [ # NV_GPU_PSTATE20_CLOCK_ENTRY_V1 
	("domainId", c_enum),
	("typeId", c_enum),
	("blsEditable", c_uint32, 1),
	("reserved", c_uint32, 31),
	("freqDelta_kHz", NvidiaParamDelta),

	("data", union('NvidiaClockEntryData', [
		('single', struct('NvidiaClockEntryDataSingle', [
			('freq_khz', c_uint32)
		])),
		('range', struct('NvidiaClockEntryDataRange', [
			("minFreq_kHz", c_uint32),
			("maxFreq_kHz", c_uint32),
			("domainId", c_enum),
			("minVoltage_uV", c_uint32),
			("maxVoltage_uV", c_uint32)
		]))
	])),
])

struct('NvidiaPerfStatesInfo', [ # NV_GPU_PERF_PSTATES20_INFO_V2
	('version', c_uint32),
	("blsEditable", c_uint32, 1),
	("reserved", c_uint32, 31),
	("numPstates", c_uint32),
	("numClocks", c_uint32),
	("numBaseVoltages", c_uint32),

	('pstates', struct('NvidiaPerfState', [
		('pStateId', c_enum),
		("blsEditable", c_uint32, 1),
		("reserved", c_uint32, 31),
		("clocks", NvidiaClockEntry * NVAPI_MAX_GPU_PSTATE20_CLOCKS),
		("baseVoltages", NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
	]) * NVAPI_MAX_GPU_PSTATE20_PSTATES),

	('voltages', struct('NvidiaOverVoltage', [
		('numVoltages', c_uint32),
		('voltages', NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES)
	]))
])