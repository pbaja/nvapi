import tkinter as tk

from .frame import InfoFrame, TuneFrame
from .constants import *


class Page:
    '''Common class for pages in application window'''
    def __init__(self, parent):
        self.mainFrame = tk.Frame(parent)

class GPUPage(Page):
    '''Page representing current state of specific GPU'''
    def __init__(self, parent):
        super().__init__(parent)
        self.info = InfoFrame(self.mainFrame)
        self.tune = TuneFrame(self.mainFrame)