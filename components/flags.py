import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_flags_with_header(frame, flags, colors, processor=None):
    container = ttk.Frame(frame)
    container.pack(fill='both', expand=True)
    container.grid_columnconfigure(0, weight=1)  # Logo
    container.grid_columnconfigure(1, weight=1)  # Title
    container.grid_columnconfigure(2, weight=1)  # PPS Counter
    container.grid_columnconfigure(3, weight=3)  # Flags

    # Logo
    img = tk.PhotoImage(file="components/msm.png")
    img = img.subsample(8, 8)
    logo_label = ttk.Label(container, image=img, style='White.TLabel')
    logo_label.image = img
    logo_label.grid(row=0, column=0, padx=10, pady=5)

    # Title
    title_label = ttk.Label(container, 
                           text="Wireless Telemetry\nDiagnostic Tool", 
                           font=("Segoe UI", 16, "bold"), 
                           foreground="red", 
                           style='White.TLabel')
    title_label.grid(row=0, column=1, padx=10, pady=5)

    # PPS Counter
    pps_frame = ttk.Frame(container, style='Black.TFrame')
    pps_frame.grid(row=0, column=2, padx=10, pady=5)
    
    pps_label = ttk.Label(pps_frame, 
                         text="PPS", 
                         font=("Segoe UI", 20, "bold"), 
                         foreground="black",
                         background="white",
                         style='White.TLabel')
    pps_label.pack()
    
    pps_value = ttk.Label(pps_frame, 
                         text="0",  # Default to 0
                         font=("Segoe UI", 25, "bold"),
                         foreground="black",
                         background="white",
                         style='White.TLabel')
    pps_value.pack()
    

    if processor:
        def update_pps():
            if hasattr(processor, 'get_pps'):
                try:
                    pps = processor.get_pps()
                    pps_value.configure(text=f"{pps:03d}")
                except:
                    pass  # Ignore errors
            # Update 4 times per second (250ms)
            container.after(250, update_pps)

        container.after(250, update_pps)


    flags_frame = ttk.Frame(container, style='Black.TFrame')
    flags_frame.grid(row=0, column=3, sticky='nsew', padx=5)


    fig, ax = plt.subplots(figsize=(12, 0.8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')


    spacing = 3.6
    triangles = []
    labels = []
    exclams = []


    for i, (flag, color) in enumerate(zip(flags, colors)):
        tri, excl, lbl = flags_icon(ax, i * spacing, color, flag[0], flag[1] == 1)
        triangles.append(tri)
        exclams.append(excl)
        labels.append(lbl)
    
    ax.set_xlim(-0.5, len(flags) * spacing + 0.5)
    ax.set_ylim(0, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout(pad=0.2)

    canvas = FigureCanvasTkAgg(fig, master=flags_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')
    

    if processor:
        # Create a function that updates flags
        def update_all_flags():

            inverter_count = len(processor.inverter_flags)
            battery_count = len(processor.battery_flags)
            imd_count = len(processor.imd_flags)
            
            all_flags = processor.inverter_flags + processor.battery_flags + processor.imd_flags
            all_colors = ['red'] * inverter_count + ['#0000FF'] * battery_count + ['#FFFF00'] * imd_count
            
            # Update all flags
            for i, (flag, color) in enumerate(zip(all_flags, all_colors)):
                if i < len(triangles):
                    triangle = triangles[i]
                    excl = exclams[i]
                    label = labels[i]
                    
                    # Update color based on flag state
                    display_color = color if flag[1] == 1 else '#808080'
                    triangle.set_edgecolor(display_color)
                    excl.set_color(display_color)
                    label.set_color(display_color)
            

            canvas.draw_idle()

        def update_inverter_flags(flags):
            update_all_flags()
            
        def update_battery_flags(flags):
            update_all_flags()
            
        def update_imd_flags(flags):
            update_all_flags()

        if hasattr(processor, 'register_flag_callback'):
            processor.register_flag_callback(update_inverter_flags)
            
        if hasattr(processor, 'register_battery_flag_callback'):
            processor.register_battery_flag_callback(update_battery_flags)
            
        if hasattr(processor, 'register_imd_flag_callback'):
            processor.register_imd_flag_callback(update_imd_flags)
    
    return container

def flags_icon(ax, x, color, code, active):
    display_color = color if active else '#808080'
    triangle = patches.Polygon([[x, 1.2], [x + 1.6, 4.2], [x + 3.2, 1.2]], 
                           closed=True, edgecolor=display_color, facecolor='none', linewidth=2)
    ax.add_patch(triangle)
    

    excl = ax.text(x + 1.6, 2, '!', fontsize=20, ha='center', va='center', 
                 color=display_color, fontname='Arial Rounded MT Bold')

    label = ax.text(x + 1.2, 0.4, code, fontsize=10, ha='center', va='center', 
                  color=display_color, fontname='Arial Rounded MT Bold')
    
    return triangle, excl, label

def update_battery_flags(self, flags_byte):
    """Update battery flags based on status byte - will be implemented when BMS data is available"""

    for i in range(len(self.battery_flags)):
        self.battery_flags[i] = (self.battery_flags[i][0], 0)

    for callback in self.battery_flag_callbacks:
        callback(self.battery_flags)

def update_imd_flags(self, flags_byte):
    """Update IMD flags based on status byte - will be implemented when IMD data is available"""

    for i in range(len(self.imd_flags)):
        self.imd_flags[i] = (self.imd_flags[i][0], 0)
    
    for callback in self.imd_flag_callbacks:
        callback(self.imd_flags)

def register_battery_flag_callback(self, callback):
    """Register a callback function to be called when battery flags change"""
    self.battery_flag_callbacks.append(callback)

def register_imd_flag_callback(self, callback):
    """Register a callback function to be called when IMD flags change"""
    self.imd_flag_callbacks.append(callback)