from tkinter import messagebox
from nvapi import NvidiaAPI, NvidiaError
from nvapi.enums import NvidiaCoolersControlMode, NvidiaClockDomain, NvidiaStatus
from .window import Window

class GPUCompat:
    fanGetMethod = 0
    fanControlMethod = 0

class Application:
    '''Interface between API and GUI'''

    def __init__(self, api:NvidiaAPI, gui:Window):
        # Save references
        self.api = api
        self.gui = gui

        # Initialize API
        self.api.init()
        self.gpus = api.getPhysicalGPUs()
        self.gpu_compat = [GPUCompat() for _ in range(len(self.gpus))]

        # Initialize GUI
        self.gui.initPages([self.gpus[x].general.getFullName() for x in range(len(self.gpus))])
        
        # Attach 'apply' callbacks
        for idx, page in enumerate(self.gui.gpu_pages):
            page.tune.onApplyClicked = lambda *args: self._applyTune(idx, *args)
            page.fan.onApplyClicked = lambda *args: self._applyFan(idx, *args)

        # Initialize one time variables
        for x, (gpu, page) in enumerate(zip(self.gpus, self.gui.gpu_pages)):
            # Clocks
            perf_states = gpu.performance.getPerfStates()
            page.tune.setCoreOffset(perf_states.pstates[0].clocks[0].freqDelta_kHz.value // 1000)
            page.tune.setMemoryOffset(perf_states.pstates[0].clocks[1].freqDelta_kHz.value // 1000)

    def _applyTune(self, gpuidx, coreOffset, memoryOffset, forceP0):
        try:
            # Grab gpu state
            gpu = self.gpus[gpuidx]
            perfStates = gpu.performance.getPerfStates()
            # Modify values
            perfStates.pstates[0].clocks[0].freqDelta_kHz.value = coreOffset * 1000
            perfStates.pstates[0].clocks[1].freqDelta_kHz.value = memoryOffset * 1000
            perfStates.numPstates = 1
            perfStates.numClocks = 2
            perfStates.numBaseVoltages = 0
            # Apply changes
            gpu.performance.setPerfStates(perfStates)
            gpu.performance.enableDynamicPstates(forceP0)
            print(f'Applied OC. gpu: {gpuidx} core: {coreOffset} memory: {memoryOffset} forceP0: {forceP0}')

        except NvidiaError as e:
            if e.status == NvidiaStatus.INVALID_USER_PRIVILEGE:
                messagebox.showerror("Unsufficient privileges", "Administrator rights are required to apply clock offsets") 
            else:
                raise e

    def _applyFan(self):
        pass

    def update(self):
        for x, (gpu, page, compat) in enumerate(zip(self.gpus, self.gui.gpu_pages, self.gpu_compat)):
            # Display current clocks
            allClocks = gpu.performance.getAllClockFrequencies()
            page.info.setCoreClock(allClocks.domain[NvidiaClockDomain.GRAPHICS].frequency // 1000)
            page.info.setMemoryClock(allClocks.domain[NvidiaClockDomain.MEMORY].frequency // 1000)

            # Display target clocks (max values available in P0 state)
            perfStates = gpu.performance.getPerfStates()
            page.tune.setCoreClock(perfStates.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000)
            page.tune.setMemoryClock(perfStates.pstates[0].clocks[1].data.range.maxFreq_kHz // 1000)

            # Display available VRAM
            memory = gpu.driver.getMemoryInfo()
            page.info.setFreeVRAM(memory.curAvailableDedicatedVideoMemory // 1024)

            # Display current performance state
            page.info.setPerfState(gpu.performance.getPerfState())

            # Display current temperature
            # TODO: What to do if there is more than one thermal probe
            thermal = gpu.thermal.getThermalSettings()
            if thermal.count > 0: page.info.setTemp(thermal.sensors[0].currentTemp)

            # Display fan speed
            # try:
                
            # except NvidiaError as e:
            #     print(f'{gpu.general.getFullName()}: {e}')


            try:
                if compat.fanGetMethod == 0:
                    # This works on GTX cards
                    settings = gpu.cooler.getCoolerSettings()
                    fanLevel = -1
                    if thermal.count > 0: fanLevel = settings.coolers[0].currentLevel
                    page.info.setFanSpeed(gpu.cooler.getTachReading(), fanLevel)
                elif compat.fanGetMethod == 1:
                    # This works on RTX cards
                    fanStatus = gpu.cooler.getClientFanCoolersStatus()
                    cooler = fanStatus.entries[0]
                    page.info.setFanSpeed(cooler.currentRPM, cooler.currentLevel)
                elif compat.fanGetMethod == 2:
                    messagebox.showinfo('Fan status error', 'Failed to get coolers status. Fan speed info will be not available.')
                    compat.fanGetMethod = -1
            except NvidiaError as e:
                if e.status != NvidiaStatus.NOT_SUPPORTED:
                    raise e
                compat.fanGetMethod += 1

            