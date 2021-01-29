from .general import GPUGeneralSettings
from .performance import GPUPerformanceSettings
from .cooler import GPUCoolerSettings
from .driver import GPUDriverSettings
from .thermal import GPUThermalSettings

class PhysicalGPU:
    '''Represents physical gpu installed in the system'''

    def __init__(self, handle, native):

        # Handle associated with specific GPU
        self.handle = handle

        # Access to the native nvapi.dll
        self.native = native

        # Wrappers
        self.general = GPUGeneralSettings(self)
        self.performance = GPUPerformanceSettings(self)
        self.cooler = GPUCoolerSettings(self)
        self.driver = GPUDriverSettings(self)
        self.thermal = GPUThermalSettings(self)
