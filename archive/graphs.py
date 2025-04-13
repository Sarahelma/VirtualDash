import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

from collections import deque
import time
import tkinter as tk

def create_rpm_graph(frame, processor):
    # Initialize data storage
    max_points = 1000  # Store more points than displayed
    time_window = 60   # Show 60 seconds of data
    latest_time = 0    # Track the latest time
    start_time = None  # Track when we first receive data
    
    rpm_data = deque(maxlen=max_points)
    time_data = deque(maxlen=max_points)
    
    # Create figure and axis
    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Create initial empty line
    line, = ax.plot([], [], color='red', linewidth=2)
    
    # Configure plot appearance
    ax.set_title('RPM vs Time', color='white', pad=10)
    ax.set_xlabel('Time (s)', color='white')
    ax.set_ylabel('RPM', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    # Set initial axis limits explicitly
    ax.set_xlim(0, time_window)  # Start at 0 and show time_window seconds
    ax.set_ylim(0, 1000)      # Initial RPM range
    
    # Initial x-axis ticks
    x_ticks = np.linspace(0, time_window, 7)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f'{x:.1f}' for x in x_ticks], color='white')
    
    for spine in ax.spines.values():
        spine.set_color('white')

    def update_frame(frame):
        nonlocal latest_time, start_time
        timestamps, values = processor.get_signal_data('erpm')
        
        if timestamps and values:
            if start_time is None:
                start_time = timestamps[0]
            
            # Use raw ERPM value
            erpm = values[-1]
            
            # Calculate relative time in seconds
            rel_time = (timestamps[-1] - start_time) / 1000.0
            latest_time = rel_time
            
            # Add new data
            time_data.append(rel_time)
            rpm_data.append(erpm)
            
            # Calculate time window
            x_min = max(0, latest_time - time_window)
            x_max = max(time_window, latest_time)
            
            # Update line data
            line.set_data(list(time_data), list(rpm_data))
            ax.set_xlim(x_min, x_max)
            
            # Get only visible data points for y-axis scaling
            visible_rpms = [rpm for t, rpm in zip(time_data, rpm_data) if x_min <= t <= x_max]
            
            if visible_rpms:
                # Set fixed y-axis range based on expected ERPM values
                y_min = 0  # ERPM shouldn't go below 0
                y_max = 8000  # Maximum expected ERPM
                ax.set_ylim(y_min, y_max)
                
                # Update y-axis ticks with evenly spaced values
                y_ticks = np.linspace(0, y_max, 6)
                ax.set_yticks(y_ticks)
                ax.set_yticks(y_ticks)
                ax.set_yticklabels([f'{int(y)}' for y in y_ticks], color='white')
        
        return [line]

    # Create canvas and animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=10,  # Update every 10ms (100 FPS) 
        blit=True,
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas

    return canvas

def draw_heatmap(frame, data, title, vmin, vmax, units):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('black')
    cmap = 'RdBu_r' if 'Voltage' in title else 'YlOrRd'
    c = ax.pcolor(data.T, cmap=cmap, vmin=vmin, vmax=vmax, edgecolors='grey', linewidths=1)
    ax.set_title(f'{title} ({units})', color='white')
    cbar = fig.colorbar(c, ax=ax)
    cbar.set_label(units, color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.ax.tick_params(colors='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.set_xticks(np.arange(data.shape[0]+1))
    ax.set_yticks(np.arange(data.shape[1]+1))
    ax.set_xlabel('Modules', color='white')
    ax.set_ylabel('Segments', color='white')
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_battery_voltage_graph(frame):
    """Create a battery voltage graph"""
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Generate placeholder data
    time_data = np.linspace(0, 10, 100)
    voltage_data = 400 + 10 * np.sin(time_data)  # Voltage around 400V
    
    # Create line plot
    ax.plot(time_data, voltage_data, color='cyan', linewidth=2)
    
    # Customize appearance
    ax.set_title('Battery Pack Voltage', color='white', pad=10)
    ax.set_xlabel('Time (s)', color='white')
    ax.set_ylabel('Voltage (V)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    # Add spines
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_battery_current_graph(frame):
    """Create a battery current graph"""
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Generate placeholder data
    time_data = np.linspace(0, 10, 100)
    current_data = 200 * np.sin(time_data)  # Current ±200A
    
    # Create line plot
    ax.plot(time_data, current_data, color='cyan', linewidth=2)
    
    # Customize appearance
    ax.set_title('Battery Pack Current', color='white', pad=10)
    ax.set_xlabel('Time (s)', color='white')
    ax.set_ylabel('Current (A)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    # Add spines
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_ac_current_graph(frame):
    fig, ax = plt.subplots(figsize=(16, 2))  # Wider but shorter for row layout
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Sample data
    time_data = np.linspace(0, 10, 100)
    current_data = 100 * np.sin(time_data * 2)  # Simulated AC current
    
    ax.plot(time_data, current_data, color='cyan', linewidth=2)
    ax.set_title('AC Current', color='white', pad=10)
    ax.set_ylabel('Current (A)', color='white')
    ax.grid(True, color='gray', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_dc_current_graph(frame):
    fig, ax = plt.subplots(figsize=(16, 2))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    time_data = np.linspace(0, 10, 100)
    current_data = 50 + 10 * np.sin(time_data * 0.5)  # Simulated DC current
    
    ax.plot(time_data, current_data, color='magenta', linewidth=2)
    ax.set_title('DC Current', color='white', pad=10)
    ax.set_ylabel('Current (A)', color='white')
    ax.grid(True, color='gray', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_voltage_graph(frame):
    fig, ax = plt.subplots(figsize=(16, 2))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    time_data = np.linspace(0, 10, 100)
    voltage_data = 48 + 2 * np.sin(time_data)  # Simulated voltage
    
    ax.plot(time_data, voltage_data, color='yellow', linewidth=2)
    ax.set_title('Voltage', color='white', pad=10)
    ax.set_ylabel('Voltage (V)', color='white')
    ax.grid(True, color='gray', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

def create_duty_cycle_graph(frame):
    fig, ax = plt.subplots(figsize=(16, 2))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    time_data = np.linspace(0, 10, 100)
    duty_data = 50 + 40 * np.sin(time_data * 0.3)  # Simulated duty cycle
    
    ax.plot(time_data, duty_data, color='green', linewidth=2)
    ax.set_title('Duty Cycle', color='white', pad=10)
    ax.set_ylabel('Duty Cycle (%)', color='white')
    ax.grid(True, color='gray', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')