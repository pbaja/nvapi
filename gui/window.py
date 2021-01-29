import tkinter as tk
import tkinter.ttk as ttk

WINDOW_TITLE = 'NvTuner'
WINDOW_SIZE = '300x350'
MAIN_FONT = ('Open Sans', 10)
MAIN_FONT_BOLD = ('Open Sans Bold', 10)
COLOR_BG0 = '#222'
COLOR_BG1 = '#333'
COLOR_FG0 = '#FFF'
COLOR_FG1 = '#FFF'

class Window:
    def __init__(self, root):

        # Setup window
        self.root = root
        self.root.tk_setPalette(background=COLOR_BG0, foreground=COLOR_FG0, activeBackground=COLOR_BG1, activeForeground=COLOR_FG1)
        self.root.geometry(WINDOW_SIZE)
        self.root.title(WINDOW_TITLE)

        # GPU pages
        self.gpu_pages_widget = ttk.Notebook(root)
        self.gpu_pages = []

    def setGPUCount(self, count):
        if count != len(self.gpu_pages):
            # Remove old pages
            for page in self.gpu_pages:
                page.grid_forget()
                page.destroy()
            self.gpu_pages.clear()

            # Create new pages
            for x in range(count):
                page = tk.Frame()
                self.gpu_pages_widget.add(page, text=f'GPU{x}')
                self.gpu_pages.append(page)

            