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
        self.root.title(WINDOW_TITLE)

        # Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background=COLOR_BG0, borderwidth=1)
        style.configure("TNotebook.Tab", background=COLOR_BG0, foreground=COLOR_TEXT, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", COLOR_BG1)])

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

        # Set min size
        self.root.minsize(100, 100)
        print(self.root.winfo_height())
        print(self.root.winfo_width())
