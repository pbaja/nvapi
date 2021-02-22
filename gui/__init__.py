import time
import tkinter as tk
from tkinter import messagebox 

from nvapi import NvidiaAPI, NvidiaError, NvidiaStatus, NvidiaClockDomain
from nvapi.enums import NvidiaCoolersControlMode
from .window import Window

class Application:

    def __init__(self):
        # Runtime variables for UI and main loop
        self.root = tk.Tk()
        self.running = False
        self.last_update = 0.0
        self._getFanMethod = 0

        # Initialize Nvidia API
        self.api = NvidiaAPI()
        self.api.init()
        self.gpus = self.api.getPhysicalGPUs()

        # Create window
        self.window = Window(self.root)
        self.window.initPages([self.gpus[x].general.getFullName() for x in range(len(self.gpus))])
        self._init()

        # Attach 'apply' callback
        for idx, page in enumerate(self.window.gpu_pages):
            page.tune.onApplyClicked = lambda *args: self._applyClicked(idx, *args)

        self.updateGui()
        self.root.minsize(width=self.root.winfo_width(), height=self.root.winfo_height())

    def _init(self):
        '''Initialize constant window values'''
        for x, gpu in enumerate(self.gpus):
            page = self.window.gpu_pages[x]

            # Clocks
            perf_states = gpu.performance.getPerfStates()
            page.tune.setCoreOffset(perf_states.pstates[0].clocks[0].freqDelta_kHz.value // 1000)
            page.tune.setMemoryOffset(perf_states.pstates[0].clocks[1].freqDelta_kHz.value // 1000)

            # Fan
            fanControl = gpu.cooler.getClientFanCoolersControl()
            cooler = fanControl.entries[0]
            page.fan.setFanMode(NvidiaCoolersControlMode(cooler.controlMode))
            page.fan.setFanSpeed(cooler.level)


    def _applyClicked(self, gpuidx, coreOffset, memoryOffset, forceP0):
        '''Apply tuning'''
        gpu = self.gpus[gpuidx]
        perfStates = gpu.performance.getPerfStates()
        perfStates.pstates[0].clocks[0].freqDelta_kHz.value = coreOffset * 1000
        perfStates.pstates[0].clocks[1].freqDelta_kHz.value = memoryOffset * 1000
        perfStates.numPstates = 1
        perfStates.numClocks = 2
        perfStates.numBaseVoltages = 0
        try:
            gpu.performance.setPerfStates(perfStates)
            gpu.performance.enableDynamicPstates(forceP0)
            print(f'Applied OC. gpu: {gpuidx} core: {coreOffset} memory: {memoryOffset} forceP0: {forceP0}')
        except NvidiaError as e:
            if e.status == NvidiaStatus.INVALID_USER_PRIVILEGE:
                messagebox.showerror("Unsufficient privileges", "Administrator rights are required to apply clock offsets") 
            else:
                raise e

    def update(self):
        '''Update window values. As it grows it will be moved to a separate file.'''
        for x, gpu in enumerate(self.gpus):
            page = self.window.gpu_pages[x]

            # Current Clocks
            allClocks = gpu.performance.getAllClockFrequencies()
            page.info.setCoreClock(allClocks.domain[NvidiaClockDomain.GRAPHICS].frequency // 1000)
            page.info.setMemoryClock(allClocks.domain[NvidiaClockDomain.MEMORY].frequency // 1000)

            # Perf states
            perfStates = gpu.performance.getPerfStates()
            page.tune.setCoreClock(perfStates.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000)
            page.tune.setMemoryClock(perfStates.pstates[0].clocks[1].data.range.maxFreq_kHz // 1000)

            # Temperature
            thermal = gpu.thermal.getThermalSettings()
            if thermal.count > 0: page.info.setTemp(thermal.sensors[0].currentTemp)
            
            # Fan control
            #fanControl = gpu.cooler.getClientFanCoolersControl()
            # fanControl.entries[0].level = 40
            # fanControl.entries[0].controlMode = NvidiaCoolersControlMode.MANUAL
            # cooler = fanControl.entries[0]
            # print(f'level: {cooler.level} mode: {NvidiaCoolersControlMode(cooler.controlMode).name}')
            # gpu.cooler.setClientFanCoolersControl(fanControl)

            # Fan speed
            try:
                if self._getFanMethod == 0:
                    # This works on GTX cards
                    page.info.setFanSpeed(gpu.cooler.getTachReading(), -1)
                elif self._getFanMethod == 1:
                    # This works on RTX cards
                    fanStatus = gpu.cooler.getClientFanCoolersStatus()
                    cooler = fanStatus.entries[0]
                    page.info.setFanSpeed(cooler.currentRPM, cooler.currentLevel)
                elif self._getFanMethod == 2:
                    messagebox.showinfo('Failed to get FAN settings. Fan speed info will be not available.')
                    self._getFanMethod = -1
            except NvidiaError as e:
                if e.status != NvidiaStatus.NOT_SUPPORTED:
                    raise e
                self._getFanMethod += 1

            # Memory
            memory = gpu.driver.getMemoryInfo()
            page.info.setFreeVRAM(memory.curAvailableDedicatedVideoMemory // 1024)

            # Other
            # page.info.setFanSpeed
            page.info.setPerfState(gpu.performance.getPerfState())

    def updateGui(self):
        self.root.update_idletasks()
        self.root.update()

    def run(self):
        '''Start (blocking) main loop'''
        try:
            # Start loop
            self.running = True
            while self.running:
                # Update data
                if time.time()-self.last_update >= 1.0:
                    self.last_update = time.time()
                    self.update()

                # Update GUI
                self.updateGui()

        except tk.TclError:
            # Stop propagation
            self.running = False
        
    def stop(self):
        '''Ends main loop if running'''
        self.running = False
