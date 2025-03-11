import tkinter as tk
import matplotlib
matplotlib.use('TkAgg') 

from gui import DashGUI
import sys

def on_closing():
    """Handle window close button event"""
    root.destroy()  
    sys.exit(0)   

if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)  
    app = DashGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()  