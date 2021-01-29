import tkinter as tk
import tkinter.ttk as ttk

from .constants import *
from .page import GPUPage


class Window:
    '''Main application window'''

    def __init__(self, root):
        # Setup window
        self.root = root
        self.root.tk_setPalette(background=COLOR_BG0, foreground=COLOR_TEXT, activeBackground=COLOR_BG0, activeForeground=COLOR_TEXT)
        #self.root.geometry(WINDOW_SIZE)
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
                page.info.setName(name)
                self.gpu_pages_widget.add(page.mainFrame, text=names[x])
                self.gpu_pages.append(page)
