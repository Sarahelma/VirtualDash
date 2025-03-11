from tkdial import Meter
from tkinter import ttk
from data import dti_temp, battery_pack
def create_motor_temp_gauge(frame):
    motor_temp_label = ttk.Label(
        frame,
        text="Motor Temp (°C)",
        font=("Arial", 20, "bold"),
        foreground="white",
        background="black"
        )
    motor_temp_label.pack(pady=5)
    motor_temp_meter = Meter(
        frame, 
        radius=440, 
        start=0, 
        end=100,
        border_width=0,
        fg="black", 
        text_color="white", 
        start_angle=225, 
        end_angle=-270,
        text_font="DS-Digital 30", 
        scale_color="white", 
        needle_color="red",
        scroll=False
        )
    motor_temp_meter.set_mark(0, 25, "#92d050")
    motor_temp_meter.set_mark(25, 40, "#FFA500")
    motor_temp_meter.set_mark(40, 100, "#FF0000")
    motor_temp_meter.set(dti_temp['motor'])
    motor_temp_meter.pack(expand=True, fill='both')

def create_battery_temp_gauge(frame):
    battery_temp_label = ttk.Label(
    frame,
    text="Battery Temp (°C)",
    font=("Arial", 20, "bold"),
    foreground="white",
    background="black"
    )
    battery_temp_label.pack(pady=5)
    battery_temp_meter = Meter(frame, radius=440, start=0, end=100, border_width=0, fg="black", text_color="white", start_angle=225, end_angle=-270, text_font="DS-Digital 30", scale_color="white", needle_color="red", scroll=False)
    battery_temp_meter.set_mark(0, 25, "#92d050")
    battery_temp_meter.set_mark(25, 40, "#FFA500")
    battery_temp_meter.set_mark(40, 100, "#FF0000")
    battery_temp_meter.set(battery_pack['temp'])
    battery_temp_meter.pack(expand=True, fill='both')

def create_speedometer(frame):
    speed_label = ttk.Label(
        frame,
        text="Speed (MPH)",
        font=("Arial", 20, "bold"),
        foreground="white",
        background="black"
    )
    speed_label.pack(pady=5)
    
    speedometer = Meter(
        frame, 
        radius=420,
        start=0, 
        end=100,
        border_width=0,
        fg="black", 
        text_color="white",
        start_angle=225, 
        end_angle=-270,
        text_font="DS-Digital 30", 
        scale_color="white", 
        needle_color="red",
        scroll=False
    )
    
    # Set color ranges
    speedometer.set_mark(0, 60, "#92d050")    # Green up to 60
    speedometer.set_mark(60, 80, "#FFA500")   # Orange 60-80
    speedometer.set_mark(80, 100, "#FF0000")  # Red above 80
    
    speedometer.pack(expand=True, fill='both')
    return speedometer

def create_voltmeter(frame):
    """Create voltmeter gauge"""
    volt_label = ttk.Label(
        frame,
        text="Voltage (V)",
        font=("Arial", 20, "bold"),
        foreground="white",
        background="black"
    )
    volt_label.pack(pady=5)
    
    voltmeter = Meter(
        frame, 
        radius=420,
        start=0, 
        end=470,
        border_width=0,
        fg="black", 
        text_color="white",
        start_angle=225, 
        end_angle=-270,
        text_font="DS-Digital 30",
        scale_color="white", 
        needle_color="red",
        scroll=False,
        major_divisions=25
    )
    
    # Set color ranges
    voltmeter.set_mark(0, 380, "#FF0000")     # Red below 380V
    voltmeter.set_mark(380, 390, "#FFA500")   # Orange 380-390V
    voltmeter.set_mark(390, 470, "#92d050")   # Green above 390V
    
    voltmeter.pack(expand=True, fill='both')
    return voltmeter