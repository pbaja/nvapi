import time
import tkinter as tk
from tkinter import messagebox 

from nvapi import NvidiaAPI, NvidiaError, NvidiaStatus, NvidiaClockDomain
from .window import Window
from .application import Application

class ApplicationManager:
    '''Takes care of the main loop, executing updates and initialization of the API and GUI.'''

    def __init__(self):
        # Runtime variables for UI and main loop
        self.root = tk.Tk()
        self.running = False
        self.last_update = 0.0

        # Initialize
        self.api = NvidiaAPI()
        self.window = Window(self.root)
        self.app = Application(self.api, self.window)

    # def update(self):
    #         # Fan control
    #         try:
    #             if self._fanControlMethod == 0:
    #                 fanControl = gpu.cooler.getClientFanCoolersControl()
    #                 # fanControl.entries[0].level = 40
    #                 # fanControl.entries[0].controlMode = NvidiaCoolersControlMode.MANUAL
    #                 cooler = fanControl.entries[0]
    #                 print(f'level: {cooler.level} mode: {NvidiaCoolersControlMode(cooler.controlMode).name}')
    #             elif self._fanControlMethod == 2:
    #                 messagebox.showinfo('Fan control error', 'Failed to set fan coolers settings.')
    #                 self._fanControlMethod = -1
    #         except NvidiaError as e:
    #             if e.status != NvidiaStatus.NOT_SUPPORTED:
    #                 raise e
    #             self._fanControlMethod += 1

    #         # gpu.cooler.setClientFanCoolersControl(fanControl)

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
                    self.app.update()

                # Update GUI
                self.updateGui()

        except tk.TclError as e:
            raise e
            # Stop propagation
            self.running = False
        finally:
            # Dispose
            self.api.dispose()
        
    def stop(self):
        '''Ends main loop if running'''
        self.running = False
