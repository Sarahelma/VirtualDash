import tkinter as tk
from tkinter import ttk
from components.dbc_graphs import create_ac_current_graph, create_dc_current_graph, create_voltage_graph, create_duty_cycle_graph
from components.flags import draw_flags_with_header
from data import battery_flags, IMD_flags

class InverterPage:
    def __init__(self, notebook, processor):

        self.frame = ttk.Frame(notebook)
        self.frame.configure(style='Black.TFrame')
        

        self.processor = processor
 
        self.inverter_flags = processor.inverter_flags
        self.battery_flags = battery_flags
        self.IMD_flags = IMD_flags
        
        self.setup_layout()
        self.setup_components()

    def setup_layout(self):
        self.frame.grid_rowconfigure(0, weight=1, minsize=30)  # Flags strip
        self.frame.grid_rowconfigure(1, weight=4)  # AC Current
        self.frame.grid_rowconfigure(2, weight=4)  # DC Current
        self.frame.grid_rowconfigure(3, weight=4)  # Voltage
        self.frame.grid_rowconfigure(4, weight=4)  # Duty Cycle
        self.frame.grid_columnconfigure(0, weight=1)

    def setup_components(self):
        self.inverter_top_strip = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.inverter_top_strip.grid(row=0, column=0, sticky='nsew')

        self.ac_current_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.ac_current_frame.grid(row=1, column=0, sticky='nsew')

        self.dc_current_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.dc_current_frame.grid(row=2, column=0, sticky='nsew')

        self.voltage_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.voltage_frame.grid(row=3, column=0, sticky='nsew')

        self.duty_cycle_frame = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.duty_cycle_frame.grid(row=4, column=0, sticky='nsew')

        draw_flags_with_header(self.inverter_top_strip, 
                             self.inverter_flags + self.battery_flags + self.IMD_flags,
                             ['red'] * len(self.inverter_flags) + 
                             ['#0000FF'] * len(self.battery_flags) + 
                             ['#FFFF00'] * len(self.IMD_flags),
                             self.processor)  
                             

        create_ac_current_graph(self.ac_current_frame, self.processor)
        create_dc_current_graph(self.dc_current_frame, self.processor)
        create_voltage_graph(self.voltage_frame, self.processor)
        create_duty_cycle_graph(self.duty_cycle_frame, self.processor)