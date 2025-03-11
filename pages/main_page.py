import tkinter as tk
from tkinter import ttk
from components.graphs import create_rpm_graph
from components.gauges import create_motor_temp_gauge, create_battery_temp_gauge, create_speedometer, create_voltmeter
from components.flags import draw_flags_with_header
from data import dti_temp, inverter_flags, battery_flags, IMD_flags  # Add imports

class MainPage:
    def __init__(self, notebook):
        # Create the frame first
        self.frame = ttk.Frame(notebook)
        self.frame.configure(style='Black.TFrame')
        
        # Initialize flags
        self.inverter_flags = inverter_flags
        self.battery_flags = battery_flags
        self.IMD_flags = IMD_flags
        
        self.setup_layout()
        self.setup_components()

    def setup_layout(self):
        self.frame.grid_rowconfigure(0, weight=1, minsize=30)
        self.frame.grid_rowconfigure(1, weight=25)
        self.frame.grid_rowconfigure(2, weight=25)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

    def setup_components(self):
        self.main_top_strip = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.main_top_strip.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.main_rect1 = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.main_rect1.grid(row=1, column=0, columnspan=4, sticky='nsew')

        self.main_rect2 = tk.Frame(self.frame, relief='solid', borderwidth=1, bg='grey')
        self.main_rect2.grid(row=2, column=0, sticky='nsew')

        self.main_rect3 = tk.Frame(self.frame, relief='solid', borderwidth=1, bg='grey')
        self.main_rect3.grid(row=2, column=1, sticky='nsew')

        self.main_rect4 = tk.Frame(self.frame, relief='solid', borderwidth=1, bg='grey')
        self.main_rect4.grid(row=2, column=2, sticky='nsew')

        self.main_rect5 = tk.Frame(self.frame, relief='solid', borderwidth=1, bg='grey')
        self.main_rect5.grid(row=2, column=3, sticky='nsew')

        # Add components
        create_rpm_graph(self.main_rect1)
        create_motor_temp_gauge(self.main_rect2)
        create_battery_temp_gauge(self.main_rect3)
        create_speedometer(self.main_rect4)
        create_voltmeter(self.main_rect5)
        draw_flags_with_header(self.main_top_strip, self.inverter_flags + self.battery_flags + self.IMD_flags,
                               ['red'] * len(self.inverter_flags) + ['#0000FF'] * len(self.battery_flags) + ['#FFFF00'] * len(self.IMD_flags))