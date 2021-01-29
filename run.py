import ctypes, os, sys
from tkinter import messagebox
from gui import Application
import subprocess as sp

if __name__ == '__main__':
    # Create window
    app = Application()

    # Check if we are running as administrator
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        result = messagebox.askyesno("Insufficient privileges", "Administrator rights are required to apply clock offsets. \nDo you want to restart as administrator?") 
        if result:
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
            sys.exit(0)

    # Start app
    app.run()