from ..constants import *
from . import Structure, Union
from . import enum, int32, uint32

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

class NvidiaClockFrequencies(Structure): # NV_GPU_CLOCK_FREQUENCIES_V2
    class NvidiaClockFrequency(Structure):
        _fields_ = [
            ('blsPresent', uint32, 1),
            ('reserved', uint32, 31),
            ('frequency', uint32)
        ]
    _fields_ = [
        ('version', uint32),
        ('clockType', uint32, 4),
        ('reserved', uint32, 20),
        ('reserved1', uint32, 8),
        ('domain', NvidiaClockFrequency * NVAPI_MAX_GPU_PUBLIC_CLOCKS),
    ]
    