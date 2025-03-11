import tkinter as tk
from tkinter import ttk
from components.graphs import create_ac_current_graph,create_dc_current_graph, create_voltage_graph, create_duty_cycle_graph
from components.flags import draw_flags_with_header
from data import dti_temp, inverter_flags, battery_flags, IMD_flags  # Add imports

class InverterPage:
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
        self.frame.grid_rowconfigure(0, weight=1, minsize=30)  # Flags strip
        self.frame.grid_rowconfigure(1, weight=20)  # AC Current
        self.frame.grid_rowconfigure(2, weight=20)  # DC Current
        self.frame.grid_rowconfigure(3, weight=20)  # Voltage
        self.frame.grid_rowconfigure(4, weight=20)  # Duty Cycle
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack_propagate(False)
    def setup_components(self):
        # Top flags strip
        self.inverter_top_strip = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.inverter_top_strip.grid(row=0, column=0, sticky='nsew')

        # Graph containers
        self.ac_current_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.ac_current_frame.grid(row=1, column=0, sticky='nsew')

        self.dc_current_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.dc_current_frame.grid(row=2, column=0, sticky='nsew')

        self.voltage_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.voltage_frame.grid(row=3, column=0, sticky='nsew')

        self.duty_cycle_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.duty_cycle_frame.grid(row=4, column=0, sticky='nsew')

        # Add components
        draw_flags_with_header(self.inverter_top_strip, 
                             self.inverter_flags + self.battery_flags + self.IMD_flags,
                             ['red'] * len(self.inverter_flags) + 
                             ['#0000FF'] * len(self.battery_flags) + 
                             ['#FFFF00'] * len(self.IMD_flags))
                             
        create_ac_current_graph(self.ac_current_frame)
        create_dc_current_graph(self.dc_current_frame)
        create_voltage_graph(self.voltage_frame)
        create_duty_cycle_graph(self.duty_cycle_frame)