from tkinter import *
import time
import tkinter.ttk as ttk
from nvapi import NvidiaAPI

FONT = ('Open Sans', 10)

def createWindow():
    root = Tk()
    root.tk_setPalette(background='#222', foreground='#FFF', activeBackground='#444', activeForeground='#FFF')
    root.geometry('300x350')
    root.title("NvTuner")
    #configureWidget(root)
    return root

def createTitle(parent, row, text):
    w = Label(parent, text=text, borderwidth=2, font=('Open Sans Semibold', 11), foreground='#999')
    w.columnconfigure(0, weight=1)
    w.grid(row=row, column=0, columnspan=2, sticky=NSEW)

def createTextRow(parent, row, label):
    # Label
    w = Label(parent, text=label, anchor=W, font=FONT)
    w.columnconfigure(0, weight=0)
    w.grid(row=row, column=0, sticky=NSEW)
    # Text
    label_text = StringVar()
    label_text.set('-')
    w = Label(parent, textvariable=label_text, font=FONT)
    w.columnconfigure(0, weight=1)
    w.grid(row=row, column=1, sticky=NSEW)
    return label_text

def createTuningRow(parent, row, label):
    # Label
    w = Label(parent, text=label, anchor=W, font=FONT)
    w.grid(row=row, column=0, sticky=NSEW)
    # Entry
    e = Entry(parent, text='', font=FONT)
    e.grid(row=row, column=1, sticky=NSEW)

def createInfoFrame(parent, labels=[]):
    # Configure
    frame = Frame(parent, bg='red')
    frame.columnconfigure(0, weight=1)
    frame.pack(anchor=N, fill=BOTH, expand=False)
    # Add widgets
    createTitle(frame, 0, 'Info')
    string_vars = []
    for idx, label in enumerate(labels):
        string_vars.append(createTextRow(frame, idx+1, label))
    # Done
    return string_vars

def createTuneFrame(parent):
    # Configure
    frame = Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.pack(anchor=N, fill=BOTH, expand=True)
    # Add widgets
    createTitle(frame, 0, 'Tuner')
    createTuningRow(frame, 1, 'Core offset')
    createTuningRow(frame, 2, 'Memory offset')
    createTuningRow(frame, 2, 'Fan speed override')
    # Done
    return frame

if __name__ == '__main__':
    # Load Nvidia DLL and Initialize
    api = NvidiaAPI(verbose=True)
    api.init()
    gpus = api.getPhysicalGPUs()

    # Create window
    root = createWindow()
    noteStyle = ttk.Style()
    noteStyle.theme_use('default')
    noteStyle.configure("TNotebook", background='#222', borderwidth=0)
    noteStyle.configure("TNotebook.Tab", background="#222", foreground='#fff', borderwidth=0)
    noteStyle.map("TNotebook.Tab", background=[("selected", '#444')])
    tabs = ttk.Notebook(root)

    # Create tabs
    strings = []
    for gpu in gpus:
        # Grab info
        gpu_name = gpu.getFullName()
        # Create tab frame
        frame = Frame(tabs)
        tabs.add(frame, text=gpu_name)
        # Create info frame
        stringvars = createInfoFrame(frame, ['Name', 'Core clock', 'Memory clock', 'Temp', 'Fan speed', 'Free VRAM', 'Perf state'])
        stringvars[0].set(gpu_name)
        strings.append(stringvars)
    tabs.pack(expand=True, fill=BOTH)

    # Run
    try:
        timer = 0
        while True:
            # Update gpu every interval
            if time.time() - timer > 1.0:
                timer = time.time()
                for i, gpu in enumerate(gpus):
                    states = gpu.getPerfStates()
                    strings[i][1].set(f'{states.pstates[0].clocks[0].data.range.maxFreq_kHz // 1000} Mhz')
                    strings[i][2].set(f'{states.pstates[0].clocks[1].data.range.maxFreq_kHz // 1000} Mhz')
                    sensors = gpu.getThermalSensors()
                    if sensors.count > 0: 
                        temp = sensors.sensors[0].currentTemp
                        strings[i][3].set(f'{temp} °C')
                        
                    #strings[i][4].set(f'')
                    #strings[i][5].set(f'')
                    strings[i][6].set(f'P{gpu.getPerfState()}')


            # Update tkinter
            root.update_idletasks()
            root.update()
    except TclError:
        pass