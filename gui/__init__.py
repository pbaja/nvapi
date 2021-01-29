import time
import tkinter as tk

from nvapi import NvidiaAPI, NvidiaError, NvidiaStatus
from .window import Window

class Application:

    def __init__(self):
        # Runtime variables for UI and main loop
        self.root = tk.Tk()
        self.running = False
        self.last_update = 0.0

        # Initialize Nvidia API
        self.api = NvidiaAPI()
        self.api.init()
        self.gpus = self.api.getPhysicalGPUs()

        # Create window
        self.window = Window(self.root)
        self.window.initPages([self.gpus[x].general.getFullName() for x in range(len(self.gpus))])

    def update(self):
        '''Update window values. As it grows it will be moved to a separate file.'''
        for x, gpu in enumerate(self.gpus):
            page = self.window.gpu_pages[x]

            # Clocks
            perf_states = gpu.performance.getPerfStates()
            page.setCoreClock(perf_states.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000)
            page.setMemoryClock(perf_states.pstates[0].clocks[1].data.range.maxFreq_kHz // 1000)

            # Temperature
            thermal = gpu.thermal.getThermalSettings()
            if thermal.count > 0: page.setTemp(thermal.sensors[0].currentTemp)
            
            # Fan speed
            try:
                page.setFanSpeed(gpu.cooler.getTachReading())
            except NvidiaError as e:
                if e.status != NvidiaStatus.NOT_SUPPORTED:
                    raise e

            # Other
            # page.setFanSpeed
            # page.setFreeVRAM
            page.setPerfState(gpu.performance.getPerfState())

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
                self.root.update_idletasks()
                self.root.update()

        except tk.TclError:
            # Stop propagation
            self.running = False
        
    def stop(self):
        '''Ends main loop if running'''
        self.running = False
