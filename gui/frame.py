import tkinter as tk
from .constants import *
from nvapi.enums import NvidiaCoolersControlMode

class Frame:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
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
        label = tk.Label(parent, text=text, borderwidth=2, font=MAIN_FONT_BOLD, background=COLOR_BG1, foreground=COLOR_TEXT_TITLE)
        label.columnconfigure(0, weight=1)
        label.grid(row=row, column=0, pady=5, columnspan=2, sticky=tk.NSEW)

    def __createLabel(self, parent, row, text):
        # Label
        label = tk.Label(parent, text=text, anchor=tk.W, font=MAIN_FONT)
        label.columnconfigure(0, weight=0)
        label.grid(row=row, column=0, padx=5, sticky=tk.NSEW)

    def _createTextRow(self, row, label):
        self.__createLabel(self.frame, row, label)
        # Text
        text = tk.Label(self.frame, text='-', anchor=tk.E, font=MAIN_FONT)
        text.columnconfigure(0, weight=1)
        text.grid(row=row, column=1, padx=5, sticky=tk.E)
        return text

    def _createEntryRow(self, row, label, validate=None):
        self.__createLabel(self.frame, row, label)
        # Entry
        entry = tk.Entry(self.frame, width=5, validate='all', font=MAIN_FONT)
        entry.columnconfigure(0, weight=1)
        entry.grid(row=row, column=1, padx=5, sticky=tk.E)
        entry.insert(0, '-')
        entry.config(bg=COLOR_BG1, borderwidth=0)
        entry.config(validatecommand=(self.frame.register(validate), '%P'))
        return entry

    def _createOptionRow(self, row, label, defaultOption, options):
        self.__createLabel(self.frame, row, label)
        variable = tk.IntVar(self.frame)
        variable.set(defaultOption)
        option = tk.OptionMenu(self.frame, variable, *options)
        option.config(bg=COLOR_BG1, activebackground=COLOR_BG1, borderwidth=0)
        option.grid(row=row, column=1, sticky=tk.E)
        return variable

    def _createCheckboxRow(self, parent, row, label):
        self.__createLabel(parent, row, label)
        # Checkbox
        var = tk.BooleanVar()
        check = tk.Checkbutton(parent, variable=var, selectcolor=COLOR_BG0)
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
        self.row_labels[3].config(text=f'{value} °C', fg=text_color)
    def setFanSpeed(self, rpm, level): 
        self.row_labels[4].config(text=f'{level} % ({rpm} RPM)')
    def setFreeVRAM(self, value): 
        self.row_labels[5].config(text=f'{value} MB')
    def setPerfState(self, value): 
        self.row_labels[6].config(text=f'P{value}')


class FanFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # Add widgets
        self._createTitle(self.frame, 0, 'Fan Control')
        self._modeRowOptions = ['Auto', 'Manual']
        self._modeRow = self._createOptionRow(1, 'Mode', 0, self._modeRowOptions)
        self._speedRow = self._createEntryRow(4, 'Speed', self._validateEntry)

    def setFanMode(self, mode:NvidiaCoolersControlMode):
        idx = int(mode)
        self._modeRow.set(self._modeRowOptions[idx])
    
    def setFanSpeed(self, speed:int):
        self._speedRow.delete(0, tk.END)
        self._speedRow.insert(0, str(speed))


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
        btn = tk.Button(self.frame, text="Apply", command=self._apply)
        btn.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)
        self.onApplyClicked = lambda *args: print(f'Apply: {args}')

    def _apply(self):
        coreOffset = int(self._coreOffsetRow.get())
        memoryOffset = int(self._memoryOffsetRow.get())
        forceP0 = self._forceStateRow.get()
        self.onApplyClicked(coreOffset, memoryOffset, forceP0)

    def setCoreClock(self, value:int): 
        self._coreTargetRow.config(text=f'{value} Mhz')
    def setMemoryClock(self, value:int): 
        self._memoryTargetRow.config(text=f'{value} Mhz')

    def setCoreOffset(self, value:int):
        self._coreOffsetRow.delete(0, tk.END)
        self._coreOffsetRow.insert(0, str(value))
    def setMemoryOffset(self, value:int):
        self._memoryOffsetRow.delete(0, tk.END)
        self._memoryOffsetRow.insert(0, str(value))