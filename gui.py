import tkinter as tk
from tkinter import ttk
from pages.main_page import MainPage
from pages.battery_page import BatteryPage
from pages.inverter_page import InverterPage
from pages.vehicle_page import VehiclePage

class DashGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dash GUI")
        self.root.configure(bg='black')
        self.setup_notebook()

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Create and add pages
        self.main_page = MainPage(self.notebook)
        self.battery_page = BatteryPage(self.notebook)
        self.inverter_page = InverterPage(self.notebook)
        self.vehicle_page = VehiclePage(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.main_page.frame, text='Main')
        self.notebook.add(self.battery_page.frame, text='Battery')
        self.notebook.add(self.inverter_page.frame, text='Inverter')
        self.notebook.add(self.vehicle_page.frame, text='Vehicle Dynamics')