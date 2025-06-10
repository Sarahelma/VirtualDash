import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')  

from gui import DashGUI
from dbc_processor import DBCProcessor 
import sys
import argparse

def on_closing():
    """Handle window close button event"""
    root.destroy() 
    sys.exit(0)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Telemetry Dashboard with DBC parsing')
    parser.add_argument('--dbc', default="bms_can_database.dbc", 
                      help='Path to DBC file')
    parser.add_argument('--port', default="COM8", 
                      help='Serial port to use')
    args = parser.parse_args()
    
    try:

        processor = DBCProcessor(port=args.port, baud=115200, dbc_path=args.dbc)
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        app = DashGUI(root, processor)
    
        root.after(100, processor.process_flag_updates, root)
        
        root.mainloop()
        
    except Exception as e:
        print(f"Startup error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        on_closing()