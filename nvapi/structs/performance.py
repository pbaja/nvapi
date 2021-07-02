from typing import Iterator
from ..constants import *
from ..enums import *
from . import Structure, Union
from . import enum, int32, uint32

class NvidiaParamDelta(Structure):
    class NvidiaValueRange(Structure):
        _fields_ = [
            ("min", int32),
            ("max", int32)
        ]
    _fields_ = [
        ("_value", int32),
        ("_valueRange", NvidiaValueRange)
    ]

    def _with_divider(self, divider):
        self._divider = divider
        return self

    @property
    def value(self):
        div = getattr(self, '_divider', 1.0)
        return self._value / div

    @property
    def min(self):
        div = getattr(self, '_divider', 1.0)
        return self._valueRange.min / div

    @property
    def max(self):
        div = getattr(self, '_divider', 1.0)
        return self._valueRange.max / div 

class NvidiaBaseVoltageEntry(Structure):  # NV_GPU_PSTATE20_BASE_VOLTAGE_ENTRY_V1 
    _fields_ = [
        ("_domainId", enum),
        ("_blsEditable", uint32, 1),
        ("__reserved", uint32, 31),
        ("_microVolts", uint32),
        ("_microVoltsDelta", NvidiaParamDelta),
    ]

    @property
    def domain(self) -> NvidiaVoltageInfoDomainId:
        return NvidiaVoltageInfoDomainId(self._domainId)

    @property
    def is_editable(self) -> bool:
        return self._blsEditable != 0

    @property
    def voltage(self) -> float:
        '''Returns base voltage'''
        return self._microVolts / 1000.0
    
    @property
    def voltage_offset(self) -> NvidiaParamDelta:
        '''Returns base voltage offset'''
        return self._microVoltsDelta._with_divider(1000.0)

class NvidiaClockEntryData(Union):
    class NvidiaClockEntryDataSingle(Structure):
        _fields_ = [
            ('freq_kHz', uint32)
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

class NvidiaClockEntry(Structure): # NV_GPU_PSTATE20_CLOCK_ENTRY_V1 
    _fields_ = [
        ("_domainId", enum),
        ("_typeId", enum),
        ("_blsEditable", uint32, 1),
        ("__reserved", uint32, 31),
        ("_freqDelta_kHz", NvidiaParamDelta),
        ("data", NvidiaClockEntryData)
    ]

    @property
    def domain(self) -> NvidiaClockDomain:
        return NvidiaClockDomain(self._domainId)

    @property
    def clock_type(self) -> NvidiaClockType:
        return NvidiaClockType(self._typeId)

    @property
    def is_editable(self) -> bool:
        return self._blsEditable != 0

    @property
    def offset(self) -> NvidiaParamDelta:
        '''Min, max and current clock offset in Mhz'''
        return self._freqDelta_kHz._with_divider(1000.0)

    @property
    def value(self) -> float:
        '''Current for this entry clock in Mhz'''
        return self.data.single.freq_kHz / 1000.0

    @property
    def max(self) -> float:
        '''Maximum clock for this entry in Mhz'''
        return self.data.range.maxFreq_kHz / 1000.0

    @property
    def min(self) -> float:
        '''Minimum clock for this entry in Mhz'''
        return self.data.range.minFreq_kHz / 1000.0

    @property
    def min_voltage(self) -> float:
        '''Minimum voltage for this entry in V'''
        return self.data.range.minVoltage_uV / 1000.0

    @property
    def max_voltage(self) -> float:
        '''Maximum voltage for this entry in V'''
        return self.data.range.maxVoltage_uV / 1000.0


class NvidiaPerfState(Structure):
    _fields_ = [
        ('_pStateId', enum),
        ("blsEditable", uint32, 1),
        ("reserved", uint32, 31),
        ("_clocks", NvidiaClockEntry * NVAPI_MAX_GPU_PSTATE20_CLOCKS),
        ("_baseVoltages", NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES),
    ]

    def _with_parent(self, parent):
        self._parent = parent
        return self

    @property
    def id(self) -> NvidiaPerfStateId:
        '''This perf state id enum, goes from P0 to P15 plus special cases'''
        return NvidiaPerfStateId(self._pStateId)

    @property
    def clocks(self) -> Iterator[NvidiaClockEntry]:
        '''Iterator with all clocks'''
        for i in range(self._parent._numClocks):
            yield self._clocks[i]

    @property
    def base_voltages(self) -> Iterator[NvidiaBaseVoltageEntry]:
        '''Iterator with all base voltages'''
        for i in range(self._parent._numBaseVoltages):
            yield self._baseVoltages[i]

class NvidiaOverVoltage(Structure):
    _fields_ = [
        ('numVoltages', uint32),
        ('voltages', NvidiaBaseVoltageEntry * NVAPI_MAX_GPU_PSTATE20_BASE_VOLTAGES)
    ]

class NvidiaPerfStatesInfo(Structure): # NV_GPU_PERF_PSTATES20_INFO_V2
    _fields_ = [
        ('version', uint32),
        ("_blsEditable", uint32, 1),
        ("__reserved", uint32, 31),
        ("_numPstates", uint32),
        ("_numClocks", uint32),
        ("_numBaseVoltages", uint32),
        ("_pstates", NvidiaPerfState * NVAPI_MAX_GPU_PSTATE20_PSTATES),
        ("_voltages", NvidiaOverVoltage)
    ]

    @property
    def is_editable(self) -> bool:
        '''True if we can use set_perf_states()'''
        return self._blsEditable != 0

    @property
    def pstates(self) -> Iterator[NvidiaPerfState]:
        '''Returns iterator containing all available perf states'''
        for i in range(self._numPstates):
            yield self._pstates[i]._with_parent(self)

    @property
    def voltages(self) -> Iterator[NvidiaBaseVoltageEntry]:
        '''Returns iterator containing all available voltage states'''
        for i in range(self._voltages.numVoltages):
            yield self._voltages.voltages[i]._with_parent(self)

class NvidiaClockFrequency(Structure):
    _fields_ = [
        ('blsPresent', uint32, 1),
        ('_reserved', uint32, 31),
        ('frequency', uint32)
    ]

class NvidiaClockFrequencies(Structure): # NV_GPU_CLOCK_FREQUENCIES_V2
    _fields_ = [
        ('version', uint32),
        ('clockType', uint32, 4),
        ('_reserved', uint32, 20),
        ('_reserved1', uint32, 8),
        ('domain', NvidiaClockFrequency * NVAPI_MAX_GPU_PUBLIC_CLOCKS),
    ]
    