import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from collections import deque
import time
import tkinter as tk

def create_erpm_graph(frame, processor):
    fig = plt.figure(figsize=(20, 4)) 
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    line, = ax.plot([], [], color='red', linewidth=2)

    ax.set_title('ERPM vs Time', color='white', pad=10)
    ax.set_xlabel('Timestamp (ms)', color='white')
    ax.set_ylabel('ERPM', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')

    reference_time = None

    def update_frame(frame):
        timestamps, values = processor.get_signal_data('Actual_ERPM')
        
        if timestamps and values:
            ax.clear()
            ax.plot(timestamps, values, color='red', linewidth=2, label='ERPM')
            
            ax.set_title('ERPM vs Time', color='white', pad=10)
            ax.set_xlabel('Timestamp (ms)', color='white')
            ax.set_ylabel('ERPM', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Matplotlib autoscaling - i tried implementing a zooming scale but didnt work 
            y_min, y_max = ax.get_ylim()
            if y_min > 0:
                ax.set_ylim(0, y_max) 
            
            # Show last 60 seconds of data
            if len(timestamps) > 1:
                time_range = 60000  # 60 seconds in milliseconds
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)

    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    
    plt.tight_layout()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=100,  # update interval
        cache_frame_data=False
    )

    frame.animation = ani
    frame.canvas = canvas

    return canvas

def create_duty_cycle_graph(frame, processor):
    """Create a duty cycle graph using DBC data - bottom graph with x-axis shown"""

    fig, ax = plt.subplots(figsize=(20, 3))  
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
 
    ax.set_title('Duty Cycle', color='white', pad=10)
    ax.set_xlabel('Timestamp (ms)', color='white')  
    ax.set_ylabel('Duty Cycle (%)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    

    plt.tight_layout()

    def update_frame(frame):

        timestamps, values = processor.get_signal_data('Actual_Duty')
        
        if timestamps and values:
            ax.clear()
            
            ax.plot(timestamps, values, color='green', linewidth=2, label='Duty Cycle')
            
            ax.set_title('Duty Cycle', color='white', pad=10)
            ax.set_xlabel('Timestamp (ms)', color='white')
            ax.set_ylabel('Duty Cycle (%)', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
        
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Removed the y-axis minimum restriction
            # Let matplotlib determine appropriate y-axis limits automatically

            if len(timestamps) > 1:
                time_range = 60000  
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)
    

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=500,
        cache_frame_data=False
    )

    frame.animation = ani
    frame.canvas = canvas
    
    return canvas

def create_voltage_graph(frame, processor):
    """Create an input voltage graph using DBC data"""
    fig, ax = plt.subplots(figsize=(20, 3))  
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.set_title('Input Voltage', color='white', pad=10)
    ax.set_xlabel('')  
    ax.set_ylabel('Voltage (V)', color='white')
    ax.tick_params(axis='x', colors='white', labelbottom=False) 
    ax.tick_params(axis='y', colors='white') 
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout(pad=0.5)

    def update_frame(frame):
        timestamps, values = processor.get_signal_data('Actual_InputVoltage')
        
        if timestamps and values:

            ax.clear()
            ax.plot(timestamps, values, color='yellow', linewidth=2, label='Input Voltage')
            
            ax.set_title('Input Voltage', color='white', pad=10)
            ax.set_xlabel('')  
            ax.set_ylabel('Voltage (V)', color='white')
            ax.tick_params(axis='x', colors='white', labelbottom=False) 
            ax.tick_params(axis='y', colors='white')  
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Removed the y-axis minimum restriction
            # Let matplotlib determine appropriate y-axis limits automatically

            if len(timestamps) > 1:
                time_range = 60000 
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)
    

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=500,
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas
    
    return canvas

def create_ac_current_graph(frame, processor):
    """Create an AC current graph using DBC data"""
    # Increase height slightly
    fig, ax = plt.subplots(figsize=(20, 3))  # Increased height from 2 to 3
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Configure plot appearance
    ax.set_title('AC Current', color='white', pad=10)
    ax.set_xlabel('')  # Hide x-axis label
    ax.set_ylabel('Current (A)', color='white')
    ax.tick_params(axis='x', colors='white', labelbottom=False)  # Hide x-axis tick labels
    ax.tick_params(axis='y', colors='white')  # Keep y-axis ticks
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    
    # Add tight_layout to reduce padding
    plt.tight_layout()

    def update_frame(frame):
        # Get data from processor
        timestamps, values = processor.get_signal_data('Actual_ACCurrent')
        
        if timestamps and values:
            # Clear the axis for full redraw
            ax.clear()
            
            # Plot data
            ax.plot(timestamps, values, color='cyan', linewidth=2, label='AC Current')
            
            # Reapply styling after clearing
            ax.set_title('AC Current', color='white', pad=10)
            ax.set_xlabel('')  # Hide x-axis label
            ax.set_ylabel('Current (A)', color='white')
            ax.tick_params(axis='x', colors='white', labelbottom=False)  # Hide x-axis tick labels
            ax.tick_params(axis='y', colors='white')  # Keep y-axis ticks
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            # Add legend
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Removed the y-axis minimum restriction
            # Let matplotlib determine appropriate y-axis limits automatically
            
            if len(timestamps) > 1:
                time_range = 60000  # Exactly 60 seconds (60000 ms)
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)
    
    # Create canvas and animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=500,
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas
    
    return canvas

def create_dc_current_graph(frame, processor):
    """Create a DC current graph using DBC data"""
    # Increase height slightly
    fig, ax = plt.subplots(figsize=(20, 3))  # Increased height from 2 to 3
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Configure plot appearance
    ax.set_title('DC Current', color='white', pad=10)
    ax.set_xlabel('')  # Hide x-axis label
    ax.set_ylabel('Current (A)', color='white')
    ax.tick_params(axis='x', colors='white', labelbottom=False)  # Hide x-axis tick labels
    ax.tick_params(axis='y', colors='white')  # Keep y-axis ticks
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')
    
    # Add tight_layout to reduce padding
    plt.tight_layout()

    def update_frame(frame):
        # Get data from processor
        timestamps, values = processor.get_signal_data('Actual_DCCurrent')
        
        if timestamps and values:
            # Clear the axis for full redraw
            ax.clear()
            
            # Plot data
            ax.plot(timestamps, values, color='magenta', linewidth=2, label='DC Current')
            
            # Reapply styling after clearing
            ax.set_title('DC Current', color='white', pad=10)
            ax.set_xlabel('')  # Hide x-axis label
            ax.set_ylabel('Current (A)', color='white')
            ax.tick_params(axis='x', colors='white', labelbottom=False)  # Hide x-axis tick labels
            ax.tick_params(axis='y', colors='white')  # Keep y-axis ticks
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
    
            if len(timestamps) > 1:
                time_range = 60000  # Exactly 60 seconds (60000 ms)
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)
    
    # Create canvas and animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=500,
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas
    
    return canvas