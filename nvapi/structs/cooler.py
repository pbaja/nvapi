from ..constants import *
from . import Structure
from . import enum, int32, uint32

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