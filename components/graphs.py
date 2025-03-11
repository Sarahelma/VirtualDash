import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

def create_rpm_graph(frame):
    rpm_counter = 0

    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    points_in_window = 200
    time_data = np.linspace(0, 10, points_in_window)
    rpm_data = np.zeros(points_in_window)
    line, = ax.plot(time_data, rpm_data, color='red', linewidth=2)

    def animate(i):
        nonlocal rpm_counter
        current_time = rpm_counter * 0.05
        rpm_data[:-1] = rpm_data[1:]
        rpm_data[-1] = 3000 * np.sin(current_time) + 4000
        time_data[:] = np.linspace(current_time - 10, current_time, points_in_window)
        ax.clear()
        ax.set_facecolor('black')
        ax.plot(time_data, rpm_data, color='red', linewidth=2)
        ax.set_xlim(current_time - 10, current_time)
        ax.set_title('RPM vs Time', color='white', pad=10)
        ax.set_xlabel('Time (s)', color='white')
        ax.set_ylabel('RPM', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, color='grey', alpha=0.3)
        ax.set_ylim(0, 8000)
        for spine in ax.spines.values():
            spine.set_color('white')
        rpm_counter += 1

    ani = FuncAnimation(fig, animate, interval=50, cache_frame_data=False)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')
    frame.animation = ani

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
    ax.set_xlabel('Cells', color='white')
    ax.set_ylabel('Modules', color='white')
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