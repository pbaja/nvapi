import tkinter as tk
import tkinter.ttk as ttk

from .constants import *
from .page import GPUPage


class Window:
    '''Main application window'''

    def __init__(self, root):
        # Setup window
        self.root = root
        #self.root.tk_setPalette(background=COLOR_BG0, foreground=COLOR_TEXT, activeBackground=COLOR_BG0, activeForeground=COLOR_TEXT)
        self.root.title(WINDOW_TITLE)


    #         /* Text */
    # --text: #fff;
    # --chat-user-name: #288ce1; /* Username color in chat */
    # --chat-date-time: #444; /* Time color in chat message */
    # --chat-msg-status: var(--chat-user-name); /* Dot color on the left of the message if f.eg. message is unread */
    # --chat-service-msg: var(--chat-user-name); /* Service message color in chat, including date between days in chat */
    # --list-user-name: #fff; /* Username color in chat list */

    # /* Links */
    # --link: #4faeff;
    # --link-hover: var(--link);
    # --link-visited: var(--link);

    # /* Backgrounds */
    # --bg-accent: #282828;
    # --bg-header: #202020;
    # --bg1: #202020;
    # --bg0: #181818;

        bg0 = '#181818' # Not selected tabs
        bg1 = '#252525' # All widgets, labels etc.
        bg2 = '#444444' # Buttons normal
        bg3 = '#464646' # Buttons hover

        

        fg0 = '#777777'
        fg1 = '#eeeeee'
        fg2 = '#dddddd'
        fg3 = '#ffffff'

        # Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('.', relief='FLAT')
        style.configure("TFrame", background=bg1, borderwidth=0)
        style.configure("TLabel", background=bg1, foreground='#fff', borderwidth=0)
        style.configure("TCheckbutton", background=bg1, borderwidth=0)

        # Buttons
        btn_text    = '#ffffff'
        btn_normal  = '#444444'
        btn_hover   = '#464646'
        btn_pressed = '#444444'
        style.configure("TButton", foreground=btn_text, borderwidth=0)
        style.map("TButton", focuscolor=[('!active', btn_normal),('pressed', btn_pressed), ('active', btn_hover)])
        style.map("TButton", background=[('!active', btn_normal),('pressed', btn_pressed), ('active', btn_hover)])

        # Tabs
        tab_text       = '#ffffff'
        tab_background = '#000000'
        tab_unselected = '#181818'
        tab_selected   = '#252525'
        style.configure("TNotebook", background=tab_background, borderwidth=0)
        style.configure("TNotebook.Tab", foreground=tab_text, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", tab_selected), ("!selected", tab_unselected)])

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
