from typing import Iterator
from ..constants import *
from ..enums import *
from . import Structure
from . import enum, int32, uint32

class NvidiaThermalSensor(Structure):
    _fields_ = [
        ("_controller", enum),
        ("_defaultMinTemp", int32),
        ("_defaultMaxTemp", int32),
        ("_currentTemp", int32),
        ("_target", enum)
    ]

    @property
    def controller(self):
        '''Enum representing type of sensor'''
        return NvidiaThermalController(self._controller)

    @property
    def target(self):
        '''Sensor target part of the gpu'''
        return NvidiaThermalTarget(self._target)

    @property
    def current(self) -> float:
        '''Current temperature of this sensor in degrees C'''
        return float(self._currentTemp)

    @property
    def max(self) -> float:
        '''Maximum temperature of this sensor in degrees C'''
        return float(self._defaultMaxTemp)

    @property
    def min(self) -> float:
        '''Minimum temperature of this sensor in degrees C'''
        return float(self._defaultMinTemp)

class NvidiaThermalSettings(Structure):
    _fields_ = [
        ("version", uint32),
        ("_count", uint32),
        ("_sensors", NvidiaThermalSensor * NVAPI_MAX_THERMAL_SENSORS_PER_GPU)
    ]

    @property
    def sensors(self) -> Iterator[NvidiaThermalSensor]:
        for i in range(self._count):
            yield self._sensors[i]