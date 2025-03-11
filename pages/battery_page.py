import tkinter as tk
from tkinter import ttk
from components.graphs import draw_heatmap, create_battery_voltage_graph, create_battery_current_graph
from components.flags import draw_flags_with_header
from data import dti_temp, inverter_flags, battery_flags, IMD_flags, cell_volts, cell_temp  # Add imports

class BatteryPage:
    def __init__(self, notebook):
        # Create the frame first
        self.frame = ttk.Frame(notebook)
        self.frame.configure(style='Black.TFrame')
        
        # Initialize data attributes
        self.inverter_flags = inverter_flags
        self.battery_flags = battery_flags
        self.IMD_flags = IMD_flags
        self.cell_volts = cell_volts
        self.cell_temp = cell_temp
        
        self.setup_layout()
        self.setup_components()

    def setup_layout(self):
        self.frame.grid_rowconfigure(0, weight=1, minsize=30)
        self.frame.grid_rowconfigure(1, weight=25)
        self.frame.grid_rowconfigure(2, weight=25)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

    def setup_components(self):
        self.battery_top_strip = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.battery_top_strip.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.battery_rect1 = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.battery_rect1.grid(row=1, column=0, sticky='nsew')

        self.battery_rect2 = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.battery_rect2.grid(row=1, column=1, sticky='nsew')

        self.battery_rect3 = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.battery_rect3.grid(row=2, column=0, sticky='nsew')

        self.battery_rect4 = ttk.Frame(self.frame, relief='solid', borderwidth=1)
        self.battery_rect4.grid(row=2, column=1, sticky='nsew')

        # Add components
        draw_flags_with_header(self.battery_top_strip, self.inverter_flags + self.battery_flags + self.IMD_flags,
                               ['red'] * len(self.inverter_flags) + ['#0000FF'] * len(self.battery_flags) + ['#FFFF00'] * len(self.IMD_flags))
        draw_heatmap(self.battery_rect1, self.cell_volts, 'Cell Voltages', 3.0, 4.2, 'V')
        draw_heatmap(self.battery_rect2, self.cell_temp, 'Cell Temperatures', 20, 40, '°C')
        create_battery_voltage_graph(self.battery_rect3)
        create_battery_current_graph(self.battery_rect4)