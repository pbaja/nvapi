import time
import tkinter as tk

from nvapi import NvidiaAPI
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
        self.window.setGPUCount(len(self.gpus))

    def update(self):
        '''Update window values. As it grows it will be moved to a separate file.'''
        pass

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
