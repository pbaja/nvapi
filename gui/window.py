import tkinter as tk
import tkinter.ttk as ttk

WINDOW_TITLE = 'NvTuner'
WINDOW_SIZE = '300x350'
MAIN_FONT = ('Open Sans', 10)
MAIN_FONT_BOLD = ('Open Sans Semibold', 11)
COLOR_BG0 = '#222'
COLOR_BG1 = '#333'
COLOR_TEXT = '#FFF'
COLOR_TEXT_TITLE = '#999'

class Page:
    '''Common class for pages in application window'''
    
    def __init__(self, parent):
        self.mainFrame = tk.Frame(parent)

    def _createTitle(self, parent, row, text):
        w = tk.Label(parent, text=text, borderwidth=2, font=MAIN_FONT_BOLD, foreground=COLOR_TEXT_TITLE)
        w.columnconfigure(0, weight=1)
        w.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW)

    def _createTextRow(self, parent, row, label):
        # Label
        label_widget = tk.Label(parent, text=label, anchor=tk.W, font=MAIN_FONT)
        label_widget.columnconfigure(0, weight=0)
        label_widget.grid(row=row, column=0, sticky=tk.NSEW)
        # Text
        text_widget = tk.Label(parent, text='-', font=MAIN_FONT)
        text_widget.columnconfigure(0, weight=1)
        text_widget.grid(row=row, column=1, sticky=tk.NSEW)
        return text_widget


class GPUPage(Page):
    '''Page representing current state of specific GPU'''
    
    def __init__(self, parent):
        super().__init__(parent)

        # Create frame
        infoFrame = tk.Frame(self.mainFrame, bg='red')
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
    def setFanSpeed(self, value): 
        self.row_labels[4].config(text=f'{value} RPM')
    def setFreeVRAM(self, value): 
        self.row_labels[5].config(text=f'{value} MB')
    def setPerfState(self, value): 
        self.row_labels[6].config(text=f'P{value}')


class Window:
    '''Main application window'''

    def __init__(self, root):
        # Setup window
        self.root = root
        self.root.tk_setPalette(background=COLOR_BG0, foreground=COLOR_TEXT, activeBackground=COLOR_BG1, activeForeground=COLOR_TEXT)
        self.root.geometry(WINDOW_SIZE)
        self.root.title(WINDOW_TITLE)

        # GPU pages
        self.gpu_pages_widget = ttk.Notebook(self.root)
        self.gpu_pages_widget.pack(expand=True, fill=tk.BOTH)
        self.gpu_pages = []

    def initPages(self, names):
        if len(self.gpu_pages) != len(names):
            # Remove old pages
            for page in self.gpu_pages:
                page.grid_forget()
                page.destroy()
            self.gpu_pages.clear()

            # Create new pages
            for x, name in enumerate(names):
                page = GPUPage(self.root)
                page.setName(name)
                self.gpu_pages_widget.add(page.mainFrame, text=names[x])
                self.gpu_pages.append(page)
