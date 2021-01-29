import ctypes


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

from .performance import NvidiaPerfStatesInfo
from .thermal import NvidiaThermalSettings
from .driver import NvidiaMemoryInfo
from .cooler import NvidiaCoolerSettings