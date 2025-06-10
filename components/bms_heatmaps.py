import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import tkinter as tk

def create_cell_voltage_graph(frame, processor, selected_row=0, selected_col=0):
    """Create a time series graph for a specific cell's voltage"""
    fig = plt.figure(figsize=(20, 4))
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    line, = ax.plot([], [], color='blue', linewidth=2)

    ax.set_title(f'Cell {selected_row}×{selected_col} Voltage vs Time', color='white', pad=10)
    ax.set_xlabel('Timestamp (ms)', color='white')
    ax.set_ylabel('Voltage (V)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')

    # Store the currently selected cell for updates
    fig.selected_cell = (selected_row, selected_col)

    # For the voltage graph update_frame function:
    def update_frame(frame):
        row, col = fig.selected_cell
        signal_name = f"CELL_{row}x{col}_Voltage"
        timestamps, values = processor.get_signal_data(signal_name)
        
        if timestamps and values:
            ax.clear()
            ax.plot(timestamps, values, color='blue', linewidth=2, label=f'Cell {row}×{col}')
            
            ax.set_title(f'Cell {row}×{col} Voltage vs Time', color='white', pad=10)
            ax.set_xlabel('Timestamp (ms)', color='white')
            ax.set_ylabel('Voltage (V)', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Matplotlib autoscaling - ERPM style
            y_min, y_max = ax.get_ylim()
            if y_min > 3.0:  # Keep minimum at 3.0V or lower
                y_min = 3.0
            ax.set_ylim(y_min, y_max)
            
            # Show last 60 seconds of data
            if len(timestamps) > 1:
                time_range = 60000  # 60 seconds in milliseconds
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)

    # Define this function BEFORE using it
    def update_cell_selection(row, col):
        fig.selected_cell = (row, col)
        ax.set_title(f'Cell {row}×{col} Voltage vs Time', color='white', pad=10)

    # Create canvas and animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    plt.tight_layout()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=100,
        cache_frame_data=False
    )

    frame.animation = ani
    frame.canvas = canvas
    frame.update_cell = update_cell_selection  # Now this is safe

    return canvas
def create_cell_temperature_graph(frame, processor, selected_row=0, selected_col=0):
    """Create a time series graph for a specific cell's temperature"""
    fig = plt.figure(figsize=(20, 4))
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    line, = ax.plot([], [], color='orange', linewidth=2)

    ax.set_title(f'Cell {selected_row}×{selected_col} Temperature vs Time', color='white', pad=10)
    ax.set_xlabel('Timestamp (ms)', color='white')
    ax.set_ylabel('Temperature (°C)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, color='grey', alpha=0.3)
    
    for spine in ax.spines.values():
        spine.set_color('white')

    # Store the currently selected cell for updates
    fig.selected_cell = (selected_row, selected_col)

    # For the temperature graph update_frame function:
    def update_frame(frame):
        row, col = fig.selected_cell
        signal_name = f"CELL_{row}x{col}_Temps"
        timestamps, values = processor.get_signal_data(signal_name)
        
        if timestamps and values:
            ax.clear()
            ax.plot(timestamps, values, color='orange', linewidth=2, label=f'Cell {row}×{col}')
            
            ax.set_title(f'Cell {row}×{col} Temperature vs Time', color='white', pad=10)
            ax.set_xlabel('Timestamp (ms)', color='white')
            ax.set_ylabel('Temperature (°C)', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, color='grey', alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_color('white')
            
            ax.legend(loc="upper left", facecolor='black', edgecolor='white', labelcolor='white')
            
            # Matplotlib autoscaling - ERPM style
            y_min, y_max = ax.get_ylim()
            if y_min > 15:  # Keep minimum at 15°C or lower
                y_min = 15
            ax.set_ylim(y_min, y_max)
            
            # Show last 60 seconds of data
            if len(timestamps) > 1:
                time_range = 60000  # 60 seconds in milliseconds
                latest = timestamps[-1]
                ax.set_xlim(max(0, latest - time_range), latest)

    # Define this function BEFORE using it
    def update_cell_selection(row, col):
        fig.selected_cell = (row, col)
        ax.set_title(f'Cell {row}×{col} Temperature vs Time', color='white', pad=10)

    # Create canvas and animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    plt.tight_layout()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig, 
        update_frame, 
        interval=100,
        cache_frame_data=False
    )

    frame.animation = ani
    frame.canvas = canvas
    frame.update_cell = update_cell_selection  # Now this is safe

    return canvas

def create_voltage_heatmap(frame, processor, voltage_graph_frame=None, temp_graph_frame=None):
    """Create a heatmap showing battery cell voltages (7 modules × 16 segments)"""
    # Initial empty data
    rows, cols = 7, 16  # 7 modules (0-6), 16 segments (0-15)
    initial_data = [[0 for _ in range(cols)] for _ in range(rows)]  # Default to nominal voltage
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Create initial heatmap
    cmap = 'RdBu_r'  # Blue-Red colormap (high voltage = blue, low = red)
    vmin, vmax = 3, 5  
    heatmap = ax.pcolor(initial_data, cmap=cmap, vmin=vmin, vmax=vmax, 
                        edgecolors='grey', linewidths=1)
    text_annotations = [[None for _ in range(cols)] for _ in range(rows)]

    # Set up title and labels
    ax.set_title('Cell Voltage (V)', color='white')
    ax.set_xlabel('Cell Number', color='white')
    ax.set_ylabel('Module Number', color='white')
    ax.tick_params(colors='white')
    
    # Set tick positions and labels
    ax.set_xticks([x + 0.5 for x in range(cols)])
    ax.set_yticks([y + 0.5 for y in range(rows)])
    ax.set_xticklabels(list(range(cols)))
    ax.set_yticklabels(list(range(rows)))
    
    # Add colorbar
    cbar = fig.colorbar(heatmap, ax=ax)
    cbar.set_label('Voltage (V)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.ax.tick_params(colors='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    
    cell_highlight = None  # Store rectangle for highlighted cell

    def update_frame(frame):
        # Create a new 2D list for updated cell voltages
        voltage_data = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Debug counter to check if any data is received
        valid_signals = 0
        
        # Update each cell with its voltage value from the processor
        for row in range(rows):
            for col in range(cols):
                signal_name = f"CELL_{row}x{col}_Voltage"
                timestamps, values = processor.get_signal_data(signal_name)
                if values and len(values) > 0:
                    valid_signals += 1
                    voltage_data[row][col] = values[-1]  # Use the latest value
        
        print(f"Valid voltage signals received: {valid_signals}/112")
        
        # Flatten the 2D list for matplotlib's pcolor
        # pcolor needs a 1D array with length = (rows*cols)
        import numpy as np
        flattened = np.array(voltage_data).flatten()
        
        # Update the heatmap
        heatmap.set_array(flattened)
        
        # Find min and max to possibly adjust the scale
        flat_values = [val for sublist in voltage_data for val in sublist]
        if flat_values:
            actual_min = min(flat_values)
            actual_max = max(flat_values)
            if actual_min < vmin or actual_max > vmax:
                heatmap.set_clim(min(actual_min, vmin), max(actual_max, vmax))
        
        # Clear existing text annotations
        for r in range(rows):
            for c in range(cols):
                if text_annotations[r][c] is not None:
                    text_annotations[r][c].remove()
                    text_annotations[r][c] = None

        # Add text annotations with values
        for r in range(rows):
            for c in range(cols):
                # Format to 2 decimal places
                value_text = f"{voltage_data[r][c]:.2f}"
                # Position text in center of cell
                text_annotations[r][c] = ax.text(
                    c + 0.5, r + 0.5, value_text,
                    ha="center", va="center",
                    fontsize=10,  # Small font
                    color="black" if voltage_data[r][c] < 4.0 else "white"  # Dynamic text color
                )
    
    def on_cell_click(event):
        if event.inaxes == ax:
            col = int(event.xdata)
            row = int(event.ydata)
            
            # Highlight the selected cell
            nonlocal cell_highlight
            if cell_highlight:
                cell_highlight.remove()
            
            cell_highlight = plt.Rectangle((col, row), 1, 1, fill=False, 
                                          edgecolor='white', linewidth=3)
            ax.add_patch(cell_highlight)
            
            # Update the time series graphs if they exist
            if voltage_graph_frame and hasattr(voltage_graph_frame, 'update_cell'):
                voltage_graph_frame.update_cell(row, col)
                

            # Refresh the canvas
            fig.canvas.draw_idle()

    # Create canvas and start animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig,
        update_frame,
        interval=1000,  # Update every second
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas
    canvas.mpl_connect('button_press_event', on_cell_click)
    
    return canvas

def create_temperature_heatmap(frame, processor, voltage_graph_frame=None, temp_graph_frame=None):
    """Create a heatmap showing battery cell temperatures (7 modules × 16 segments)"""
    # Initial empty data
    rows, cols = 7, 16  # 7 modules (0-6), 16 segments (0-15) 
    initial_data = [[0 for _ in range(cols)] for _ in range(rows)]  # Default to room temperature
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Create initial heatmap
    cmap = 'YlOrRd'  # Yellow-Orange-Red colormap for temperature
    vmin, vmax = 20, 30  
    heatmap = ax.pcolor(initial_data, cmap=cmap, vmin=vmin, vmax=vmax, 
                        edgecolors='grey', linewidths=1)
    text_annotations = [[None for _ in range(cols)] for _ in range(rows)]

    # Set up title and labels
    ax.set_title('Cell Temperature (°C)', color='white')
    ax.set_xlabel('Cell Number', color='white')
    ax.set_ylabel('Module Number', color='white')
    ax.tick_params(colors='white')
    
    # Set tick positions and labels
    ax.set_xticks([x + 0.5 for x in range(cols)])
    ax.set_yticks([y + 0.5 for y in range(rows)])
    ax.set_xticklabels(list(range(cols)))
    ax.set_yticklabels(list(range(rows)))
    
    # Add colorbar
    cbar = fig.colorbar(heatmap, ax=ax)
    cbar.set_label('Temperature (°C)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    cbar.ax.tick_params(colors='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    plt.tight_layout()
    
    cell_highlight = None  # Store rectangle for highlighted cell

    def update_frame(frame):
        # Create a new 2D list for updated cell temperatures
        temp_data = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Update each cell with its temperature value from the processor
        for row in range(rows):
            for col in range(cols):
                signal_name = f"CELL_{row}x{col}_Temps"
                timestamps, values = processor.get_signal_data(signal_name)
                if values and len(values) > 0:
                    temp_data[row][col] = values[-1]  # Use the latest value
        
        # Flatten the 2D list for matplotlib's pcolor

        flattened = np.array(temp_data).flatten()
        
        # Update the heatmap
        heatmap.set_array(flattened)
        
        # Find min and max to possibly adjust the scale
        flat_values = [val for sublist in temp_data for val in sublist]
        if flat_values:
            actual_min = min(flat_values)
            actual_max = max(flat_values)
            if actual_min < vmin or actual_max > vmax:
                heatmap.set_clim(min(actual_min, vmin), max(actual_max, vmax))
        
        # Clear existing text annotations
        for r in range(rows):
            for c in range(cols):
                if text_annotations[r][c] is not None:
                    text_annotations[r][c].remove()
                    text_annotations[r][c] = None

        # Add text annotations with values
        for r in range(rows):
            for c in range(cols):
                # Format to 1 decimal place for temperature
                value_text = f"{temp_data[r][c]:.1f}"
                # Position text in center of cell
                text_annotations[r][c] = ax.text(
                    c + 0.5, r + 0.5, value_text,
                    ha="center", va="center",
                    fontsize=10,  # Small font
                    color="black" if temp_data[r][c] < 35 else "white"  # Dynamic text color
                )
    
    def on_cell_click(event):
        if event.inaxes == ax:
            col = int(event.xdata)
            row = int(event.ydata)
            
            # Highlight the selected cell
            nonlocal cell_highlight
            if cell_highlight:
                cell_highlight.remove()
            
            cell_highlight = plt.Rectangle((col, row), 1, 1, fill=False, 
                                          edgecolor='white', linewidth=3)
            ax.add_patch(cell_highlight)
            
            # Update the time series graphs if they exist
            if voltage_graph_frame and hasattr(voltage_graph_frame, 'update_cell'):
                voltage_graph_frame.update_cell(row, col)
                
            if temp_graph_frame and hasattr(temp_graph_frame, 'update_cell'):
                temp_graph_frame.update_cell(row, col)
            
            # Refresh the canvas
            fig.canvas.draw_idle()

    # Create canvas and start animation
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    ani = FuncAnimation(
        fig,
        update_frame,
        interval=1000,  # Update every second
        cache_frame_data=False
    )
    
    # Store references to prevent garbage collection
    frame.animation = ani
    frame.canvas = canvas
    canvas.mpl_connect('button_press_event', on_cell_click)
    
    return canvas