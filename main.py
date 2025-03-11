import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing other matplotlib components

from gui import DashGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Proper cleanup on close
    app = DashGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()