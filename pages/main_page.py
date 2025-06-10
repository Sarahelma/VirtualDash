import tkinter as tk
from tkinter import ttk
from components.dbc_graphs import create_erpm_graph
from components.gauges import create_motor_temp_gauge, create_battery_temp_gauge, create_speedometer, create_voltmeter
from components.flags import draw_flags_with_header
from data import battery_flags, IMD_flags

class MainPage:
    def __init__(self, notebook, processor):

        self.frame = ttk.Frame(notebook)
        self.frame.configure(style='Black.TFrame')
        

        self.processor = processor
        

        self.inverter_flags = processor.inverter_flags
        self.battery_flags = processor.battery_flags
        self.IMD_flags = processor.imd_flags
        
 
        self.gauges = {}
        
        # Setup conversion for ERPM to KPH
        self.erpm_to_kph = lambda erpm: (erpm / (10 * 3.9 )) * 45.72 * 3.1416 * 60 / 160934.4
        self.setup_layout()
        self.setup_components()
        self.setup_gauge_updates()

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


        create_erpm_graph(self.main_rect1, self.processor)  

        self.gauges['motor_temp'] = create_motor_temp_gauge(self.main_rect2)
        self.gauges['battery_temp'] = create_battery_temp_gauge(self.main_rect3)
        self.gauges['speed'] = create_speedometer(self.main_rect4)
        self.gauges['voltage'] = create_voltmeter(self.main_rect5)
        
        draw_flags_with_header(self.main_top_strip, 
                             self.inverter_flags + self.battery_flags + self.IMD_flags,
                             ['red'] * len(self.inverter_flags) + 
                             ['#0000FF'] * len(self.battery_flags) + 
                             ['#FFFF00'] * len(self.IMD_flags),
                             self.processor)

    def setup_gauge_updates(self):
        """Setup periodic updates for gauges from DBC data"""
        
        def update_gauges():

            _, motor_temp_values = self.processor.get_signal_data('Actual_TempMotor')
            if motor_temp_values:

                motor_temp = motor_temp_values[-1]
                self.gauges['motor_temp'].set(motor_temp)
            
            _, voltage_values = self.processor.get_signal_data('Actual_InputVoltage') 
            if voltage_values:
                voltage = voltage_values[-1]
                self.gauges['voltage'].set(voltage)

            _, erpm_values = self.processor.get_signal_data('Actual_ERPM')
            if erpm_values:
                erpm = erpm_values[-1]
                speed_kph = self.erpm_to_kph(erpm)
                self.gauges['speed'].set(speed_kph)
                

            self.frame.after(250, update_gauges)  # Update 4 times per second
            
        self.frame.after(250, update_gauges)