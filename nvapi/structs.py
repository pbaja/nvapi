import ctypes, sys, inspect
from .defines import *

# Data types

enum = ctypes.c_int32
int32 = ctypes.c_int32
uint32 = ctypes.c_uint32

# Base classes

def _getitem(self, i):
	name = self._fields_[i][0]
	value = getattr(self, name)
	if isinstance(value, Structure) or isinstance(value, Union):
		value = dict(value)
	return (name, value)

class Union(ctypes.Union):
	def __getitem__(self, i):
		return _getitem(self, i)

class Structure(ctypes.Structure):
	def __getitem__(self, i):
		return _getitem(self, i)

# Structures

class NvidiaThermalSettings(Structure):
	class NvidiaThermalSensor(Structure):
		_fields_ = [
			("controller", enum),
			("defaultMinTemp", int32),
			("defaultMaxTemp", int32),
			("currentTemp", int32),
			("target", enum)
		]
	_fields_ = [
		("version", uint32),
		("count", uint32),
		("sensors", NvidiaThermalSensor * NVAPI_MAX_THERMAL_SENSORS_PER_GPU)
	]

class NvidiaCoolerSettings(Structure):
	class NvidiaCooler(Structure):
		_fields_ = [
			("type", enum),
			("controller", enum),
			("defaultMinLevel", uint32),
			("defaultMaxLevel", uint32),
			("currentMinLevel", uint32),
			("currentMaxLevel", uint32),
			("currentLevel", uint32),
			("defaultPolicy", enum),
			("currentPolicy", enum),
			("target", enum),
			("controlMode", enum),
			("active", uint32)
		]
	_fields_ = [
		("version", uint32),
		("count", uint32),
		("coolers", NvidiaCooler * NVAPI_MAX_COOLERS_PER_GPU)
	]

class NvidiaMemoryInfo(Structure):
	_fields_ = [
		("version", uint32),
		("dedicatedVideoMemory", uint32),
		("availableDedicatedVideoMemory", uint32),
		("systemVideoMemory", uint32),
		("sharedSystemMemory", uint32),
		("curAvailableDedicatedVideoMemory", uint32),
		("dedicatedVideoMemoryEvictionsSize", uint32),
		("dedicatedVideoMemoryEvictionCount", uint32)
	]

class NvidiaParamDelta(Structure):
	class NvidiaValueRange(Structure):
		_fields_ = [
			("min", int32),
			("max", int32)
		]
	_fields_ = [
		("value", int32),
		("valueRange", NvidiaValueRange)
	]

class NvidiaBaseVoltageEntry(Structure):  # NV_GPU_PSTATE20_BASE_VOLTAGE_ENTRY_V1 
	_fields_ = [
		("domainId", enum),
		("blsEditable", uint32, 1),
		("reserved", uint32, 31),
		("volt_uV", uint32),
		("voltDelta_uV", NvidiaParamDelta),
	]

class NvidiaClockEntry(Structure): # NV_GPU_PSTATE20_CLOCK_ENTRY_V1 
	class NvidiaClockEntryData(Union):
		class NvidiaClockEntryDataSingle(Structure):
			_fields_ = [
				('freq_khz', uint32)
			]
		class NvidiaClockEntryDataRange(Structure):
			_fields_ = [
				("minFreq_kHz", uint32),
				("maxFreq_kHz", uint32),
				("domainId", enum),
				("minVoltage_uV", uint32),
				("maxVoltage_uV", uint32)
			]
		_fields_ = [
			("min", int32),
			("max", int32),
			("single", NvidiaClockEntryDataSingle),
			("range", NvidiaClockEntryDataRange)
		]
	_fields_ = [
		("domainId", enum),
		("typeId", enum),
		("blsEditable", uint32, 1),
		("reserved", uint32, 31),
		("freqDelta_kHz", NvidiaParamDelta),
		("data", NvidiaClockEntryData)
	]

class NvidiaPerfStatesInfo(Structure): # NV_GPU_PERF_PSTATES20_INFO_V2
	class NvidiaPerfState(Structure):
		_fields_ = [
			('pStateId', enum),
			("blsEditable", uint32, 1),
			("reserved", uint32, 31),
			("clocks", NvidiaClockEntry * NVAPI_MAX_GPU_PSTATE20_CLOCKS),
			("baseVoltages", NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
		]
	class NvidiaOverVoltage(Structure):
		_fields_ = [
			('numVoltages', uint32),
			('voltages', NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES)
		]
	_fields_ = [
		('version', uint32),
		("blsEditable", uint32, 1),
		("reserved", uint32, 31),
		("numPstates", uint32),
		("numClocks", uint32),
		("numBaseVoltages", uint32),
		("pstates", NvidiaPerfState * NVAPI_MAX_GPU_PSTATE20_PSTATES),
		("voltages", NvidiaOverVoltage)
	]