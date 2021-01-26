from tkinter import *

def createRoot():
    root = Tk()
    root.tk_setPalette(background='#222', foreground='#FFF', activeBackground='#444', activeForeground='#FFF')
    root.geometry('300x350')
    return root

def createTitle(parent, row, text):
    w = Label(parent, text=text, borderwidth=2, font=('Segoe UI', 10), bg='#333')
    w.grid(row=row, column=0, columnspan=2, sticky=W+E)

def createTextRow(parent, row, label, text):
    # Label
    w = Label(parent, text=label, anchor=W, font=('Segoe UI', 10))
    w.grid(row=row, column=0, sticky=W+E)
    # Text
    w = Label(parent, text=text, font=('Segoe UI', 10))
    w.grid(row=row, column=1, sticky=W+E)

def createEntryRow(parent, row, label):
    # Label
    w = Label(parent, text=label, anchor=W, font=('Segoe UI', 10))
    w.grid(row=row, column=0, sticky=W+E)
    # Entry
    e = Entry(parent, text='', font=('Segoe UI', 10))
    e.grid(row=row, column=1, sticky=W+E)

def createInfoFrame(root):
    frame = Frame(root)
    frame.pack(expand=True, anchor=N)
    createTitle(frame, 0, 'Info')
    createTextRow(frame, 1, 'Name', 'GeForce RTX3060 Ti')
    createTextRow(frame, 2, 'Core clock', '1234 Mhz')
    createTextRow(frame, 3, 'Memory clock', '4321 Mhz')
    createTextRow(frame, 6, 'Temp', '73 °C')
    createTextRow(frame, 5, 'Free VRAM', '6.7 GB')
    createTextRow(frame, 4, 'Perf state', 'P2')

def createTuneFrame(root):
    frame = Frame(root)
    frame.pack(expand=True, anchor=N)
    createTitle(frame, 0, 'Tuner')
    createEntryRow(frame, 1, 'Core offset')
    createEntryRow(frame, 2, 'Memory offset')

root = createRoot()
createInfoFrame(root)
createTuneFrame(root)
root.mainloop()