import tkinter as tk
from tkinter import ttk
from pages.main_page import MainPage
from pages.battery_page import BatteryPage
from pages.inverter_page import InverterPage
from pages.vehicle_page import VehiclePage

class DashGUI:
    def __init__(self, root, processor):
        self.root = root
        self.processor = processor  # Store processor instance
        self.root.title("Dash GUI")
        self.root.configure(bg='black')
        self.setup_notebook()
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[30, 10])  # [width, height]
        
    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create and add pages with processor instance
        self.main_page = MainPage(self.notebook, self.processor)
        self.battery_page = BatteryPage(self.notebook, self.processor)
        self.inverter_page = InverterPage(self.notebook, self.processor)
        self.vehicle_page = VehiclePage(self.notebook, self.processor)

        # Add frames to notebook
        self.notebook.add(self.main_page.frame, text='Main')
        self.notebook.add(self.battery_page.frame, text='Battery')
        self.notebook.add(self.inverter_page.frame, text='Inverter')
        self.notebook.add(self.vehicle_page.frame, text='Vehicle Dynamics')

    # Add to DashGUI class
    def pause_inactive_tab_updates(self, active_tab):
        self.updating_tabs = False
        # Allow time for tab rendering to complete
        self.root.after(200, self.resume_updates, active_tab)

    def resume_updates(self, active_tab):
        self.updating_tabs = True
        # Resume updates only for the active tab
        # Your implementation depends on how your pages are structured