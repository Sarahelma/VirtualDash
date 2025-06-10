import tkinter as tk
from tkinter import ttk
from components.flags import draw_flags_with_header
from components.bms_heatmaps import create_voltage_heatmap, create_temperature_heatmap, create_cell_voltage_graph, create_cell_temperature_graph
from data import dti_temp, inverter_flags, battery_flags, IMD_flags, cell_volts, cell_temp
import matplotlib.pyplot as plt

class BatteryPage:
    def __init__(self, notebook, processor):
        self.frame = ttk.Frame(notebook)
        self.frame.configure(style='Black.TFrame')
        self.processor = processor 
        
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

        # Add flags header with processor
        draw_flags_with_header(self.battery_top_strip, 
                              self.inverter_flags + self.battery_flags + self.IMD_flags,
                              ['red'] * len(self.inverter_flags) + 
                              ['#0000FF'] * len(self.battery_flags) + 
                              ['#FFFF00'] * len(self.IMD_flags),
                              self.processor)
        
        # First, create the cell-specific time series graphs
        # Initial default cell (0,0)
        voltage_graph = create_cell_voltage_graph(self.battery_rect3, self.processor)
        temp_graph = create_cell_temperature_graph(self.battery_rect4, self.processor)
        
        # Now create the heatmaps with references to the graph frames
        # This allows heatmap clicks to update the time series graphs
        create_voltage_heatmap(self.battery_rect1, self.processor,
                              self.battery_rect3, self.battery_rect4)
        create_temperature_heatmap(self.battery_rect2, self.processor,
                                  self.battery_rect3, self.battery_rect4)