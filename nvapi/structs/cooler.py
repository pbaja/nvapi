from ..constants import *
from . import Structure
from . import enum, int32, uint32
import ctypes

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

class NvidiaFanCoolersStatus(Structure):
    class NvidiaFanCoolersStatusEntry(Structure):
        _fields_ = [
            ('idx', uint32),
            ('currentRPM', uint32),
            ('minLevel', uint32),
            ('maxLevel', uint32),
            ('currentLevel', uint32),
            ('reserved', uint32 * 8)
        ]
    _fields_ = [
        ('version', uint32),
        ('count', uint32),
        ('reserved', uint32 * 8),
        ('entries', NvidiaFanCoolersStatusEntry * NVAPI_MAX_FAN_COOLER_STATUS_ENRIES)
    ]

class NvidiaFanCoolersControl(Structure):
    class NvidiaFanCoolersControlEntry(Structure):
        _fields_ = [
            ('idx', uint32),
            ('level', uint32),
            ('controlMode', enum),
            ('reserved', uint32 * 8),
        ]
    _fields_ = [
        ('version', uint32),
        ('_placeholder', uint32),
        ('count', uint32),
        ('reserved', uint32 * 8),
        ('entries', NvidiaFanCoolersControlEntry * NVAPI_MAX_FAN_COOLER_CONTROL_ENRIES)
    ]