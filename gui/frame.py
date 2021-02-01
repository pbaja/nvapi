import tkinter as tk
from tkinter import ttk

from .constants import *


class Frame:
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(anchor=tk.S, side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

    def _validateEntry(self, value):
        try:
            if len(value) != 0:
                int(value)
            if len(value) > 1 and (value[0] == '0' or value[0] == ' ' or value[-1] == ' '):
                return False
            return True
        except:
            return False

    def _createTitle(self, parent, row, text):
        label = ttk.Label(parent, text=text)
        label.columnconfigure(0, weight=2)
        label.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW)

    def __createLabel(self, parent, row, text):
        # Label
        label = ttk.Label(parent, text=text, anchor=tk.W)
        label.columnconfigure(0, weight=0)
        label.grid(row=row, column=0, sticky=tk.NSEW)

    def _createTextRow(self, row, label):
        self.__createLabel(self.frame, row, label)
        # Text
        text = ttk.Label(self.frame, text='-')
        text.columnconfigure(0, weight=1)
        text.grid(row=row, column=1, sticky=tk.NSEW)
        return text

    def _createEntryRow(self, row, label, validate=None):
        self.__createLabel(self.frame, row, label)
        # Entry
        entry = tk.Entry(self.frame, validate='all')
        entry.columnconfigure(0, weight=1)
        entry.grid(row=row, column=1, sticky=tk.E)
        entry.insert(0, '-')
        entry.config(validatecommand=(self.frame.register(validate), '%P'))
        return entry

    def _createOptionRow(self, row, label, defaultOption, options):
        self.__createLabel(self.frame, row, label)
        variable = tk.StringVar(self.frame)
        variable.set(options[defaultOption])
        option = ttk.OptionMenu(self.frame, variable, *options)
        option.grid(row=row, column=1, sticky=tk.E)
        return variable

    def _createCheckboxRow(self, parent, row, label):
        self.__createLabel(parent, row, label)
        # Checkbox
        var = tk.BooleanVar()
        check = ttk.Checkbutton(parent, text='asd', variable=var)
        check.grid(row=row, column=1, sticky=tk.E)
        return var


class InfoFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Add widgets
        self.row_labels = []
        self._createTitle(self.frame, 0, 'Info')
        for i, row_name in enumerate(['Name', 'Core clock', 'Memory clock', 'Temp', 'Fan speed', 'Free VRAM', 'Perf state']):
            self.row_labels.append(self._createTextRow(i+1, row_name))

    def setName(self, value):
        self.row_labels[0].config(text=value)
    def setCoreClock(self, value): 
        self.row_labels[1].config(text=f'{value} Mhz')
    def setMemoryClock(self, value): 
        self.row_labels[2].config(text=f'{value} Mhz')
    def setTemp(self, value): 
        text_color = COLOR_TEXT
        if value < 20: text_color = 'cyan'
        elif value > 90: text_color = 'red'
        elif value > 80: text_color = 'orange'
        self.row_labels[3].config(text=f'{value} °C', foreground=text_color)
    def setFanSpeed(self, rpm, level): 
        fan_str = '?'
        if rpm == -1: fan_str = f'{level} %'
        elif level == -1: fan_str = f'{rpm} RPM'
        else: fan_str = f'{level} % ({rpm} RPM)'
        self.row_labels[4].config(text=fan_str)
    def setFreeVRAM(self, value): 
        self.row_labels[5].config(text=f'{value} MB')
    def setPerfState(self, value): 
        self.row_labels[6].config(text=f'P{value}')


class FanFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Add widgets
        self._createTitle(self.frame, 0, 'Fan Control')
        self._createOptionRow(1, 'Mode', 0, ['Auto', 'Manual'])
        self._createEntryRow(4, 'Speed', self._validateEntry)

class TuneFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Add widgets
        self._createTitle(self.frame, 0, 'Tune')
        self._coreTargetRow = self._createTextRow(1, 'Core target')
        self._coreOffsetRow = self._createEntryRow(2, 'Core offset', self._validateEntry)
        self._memoryTargetRow = self._createTextRow(3, 'Memory target')
        self._memoryOffsetRow = self._createEntryRow(4, 'Memory offset', self._validateEntry)
        self._forceStateRow = self._createCheckboxRow(self.frame, 5, 'Force P0 state')
        # Add button
        btn = ttk.Button(self.frame, text="Apply", command=self._apply)
        btn.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)
        self.onApplyClicked = lambda *args: print(f'Apply: {args}')

    def _apply(self):
        coreOffset = int(self._coreOffsetRow.get())
        memoryOffset = int(self._memoryOffsetRow.get())
        forceP0 = self._forceStateRow.get()
        self.onApplyClicked(coreOffset, memoryOffset, forceP0)

    def setCoreClock(self, value): 
        self._coreTargetRow.config(text=f'{value} Mhz')
    def setMemoryClock(self, value): 
        self._memoryTargetRow.config(text=f'{value} Mhz')

    def setCoreOffset(self, value):
        self._coreOffsetRow.delete(0, tk.END)
        self._coreOffsetRow.insert(0, str(value))
    def setMemoryOffset(self, value):
        self._memoryOffsetRow.delete(0, tk.END)
        self._memoryOffsetRow.insert(0, str(value))