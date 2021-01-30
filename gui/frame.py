import tkinter as tk

from .constants import *


class Frame:
    
    def _createTitle(self, parent, row, text):
        label = tk.Label(parent, text=text, borderwidth=2, font=MAIN_FONT_BOLD, foreground=COLOR_TEXT_TITLE)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW)

    def __createLabel(self, parent, row, label):
        # Label
        label = tk.Label(parent, text=label, anchor=tk.W, font=MAIN_FONT)
        label.columnconfigure(0, weight=0)
        label.grid(row=row, column=0, sticky=tk.NSEW)

    def _createTextRow(self, parent, row, label):
        self.__createLabel(parent, row, label)
        # Text
        text = tk.Label(parent, text='-', font=MAIN_FONT)
        text.columnconfigure(0, weight=1)
        text.grid(row=row, column=1, sticky=tk.NSEW)
        return text

    def _createEntryRow(self, parent, row, label, validate=None):
        self.__createLabel(parent, row, label)
        # Entry
        entry = tk.Entry(parent, width=5, validate='all', font=MAIN_FONT)
        entry.columnconfigure(0, weight=1)
        entry.grid(row=row, column=1, pady=5, padx=50, sticky=tk.NSEW)
        entry.insert(0, '-')
        entry.config(validatecommand=(parent.register(validate), '%P'))
        return entry

    def _createCheckboxRow(self, parent, row, label):
        self.__createLabel(parent, row, label)
        # Checkbox
        var = tk.BooleanVar()
        check = tk.Checkbutton(parent, variable=var, selectcolor=COLOR_BG0)
        check.grid(row=row, column=1, sticky=tk.NSEW)
        return var

class InfoFrame(Frame):

    def __init__(self, parent):
        # Create frame
        infoFrame = tk.Frame(parent)
        infoFrame.columnconfigure(0, weight=1)
        infoFrame.pack(anchor=tk.N, fill=tk.BOTH, expand=False)
        # Add widgets
        self.row_labels = []
        self._createTitle(infoFrame, 0, 'Info')
        for i, row_name in enumerate(['Name', 'Core clock', 'Memory clock', 'Temp', 'Fan speed', 'Free VRAM', 'Perf state']):
            self.row_labels.append(self._createTextRow(infoFrame, i+1, row_name))

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
        self.row_labels[3].config(text=f'{value} °C', fg=text_color)
    def setFanSpeed(self, rpm, level): 
        self.row_labels[4].config(text=f'{level} % ({rpm} RPM)')
    def setFreeVRAM(self, value): 
        self.row_labels[5].config(text=f'{value} MB')
    def setPerfState(self, value): 
        self.row_labels[6].config(text=f'P{value}')

class TuneFrame(Frame):

    def __init__(self, parent):
        # Create frame
        infoFrame = tk.Frame(parent)
        infoFrame.columnconfigure(0, weight=1)
        infoFrame.pack(anchor=tk.N, fill=tk.BOTH, expand=False)
        # Add widgets
        self.row_entries = []
        self._createTitle(infoFrame, 0, 'Tune')
        self._coreTargetRow = self._createTextRow(infoFrame, 1, 'Core target')
        self._coreOffsetRow = self._createEntryRow(infoFrame, 2, 'Core offset', self._validateEntry)
        self._memoryTargetRow = self._createTextRow(infoFrame, 3, 'Memory target')
        self._memoryOffsetRow = self._createEntryRow(infoFrame, 4, 'Memory offset', self._validateEntry)
        self._forceStateRow = self._createCheckboxRow(infoFrame, 5, 'Force P0 state')
        # Add button
        btn = tk.Button(infoFrame, text="Apply", command=self._apply)
        btn.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)
        self.onApplyClicked = lambda *args: print(f'Apply: {args}')

    def _apply(self):
        coreOffset = int(self._coreOffsetRow.get())
        memoryOffset = int(self._memoryOffsetRow.get())
        forceP0 = self._forceStateRow.get()
        self.onApplyClicked(coreOffset, memoryOffset, forceP0)

    def _validateEntry(self, value):
        try:
            if len(value) != 0:
                int(value)
            if len(value) > 1 and (value[0] == '0' or value[0] == ' ' or value[-1] == ' '):
                return False
            return True
        except:
            return False

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