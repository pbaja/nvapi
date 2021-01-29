from ..constants import *
from . import Structure
from . import enum, int32, uint32

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