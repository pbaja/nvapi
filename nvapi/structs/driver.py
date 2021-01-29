from . import Structure
from . import enum, int32, uint32

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

