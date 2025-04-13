import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from archive.serialparse import telemetry
import time

def create_monitoring_window():
    # Setup the plotting window
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.patch.set_facecolor('black')
    
    # Create lines for each data type
    lines = {
        'ac': ax1.plot([], [], 'c-', label='AC Current')[0],
        'dc': ax2.plot([], [], 'r-', label='DC Current')[0],
        'temp': ax3.plot([], [], 'y-', label='Motor Temp')[0],
        'duty': ax4.plot([], [], 'm-', label='Duty Cycle')[0]
    }
    
    # Configure all axes
    for ax, title in zip([ax1, ax2, ax3, ax4], 
                        ['AC Current', 'DC Current', 
                         'Motor Temperature', 'Duty Cycle']):
        ax.set_facecolor('black')
        ax.grid(True, color='gray', alpha=0.3)
        ax.tick_params(colors='white')
        ax.set_title(title, color='white')
        ax.legend(loc='upper right')
        for spine in ax.spines.values():
            spine.set_color('white')

    def update(frame):
        try:
            # Get latest data
            ac_data = telemetry.get_plot_data('ac_current')
            dc_data = telemetry.get_plot_data('dc_current')
            temp_data = telemetry.get_plot_data('motor_temp')
            duty_data = telemetry.get_plot_data('duty')
            
            # Update lines if data exists
            if ac_data and len(ac_data) == 2:
                lines['ac'].set_data(*ac_data)
                ax1.relim()
                ax1.autoscale_view()
                
            if dc_data and len(dc_data) == 2:
                lines['dc'].set_data(*dc_data)
                ax2.relim()
                ax2.autoscale_view()
                
            if temp_data and len(temp_data) == 2:
                lines['temp'].set_data(*temp_data)
                ax3.relim()
                ax3.autoscale_view()
                
            if duty_data and len(duty_data) == 2:
                lines['duty'].set_data(*duty_data)
                ax4.relim()
                ax4.autoscale_view()
            
            # Update PPS counter in title
            fig.suptitle(f'Packets Per Second: {telemetry.pps_counter}', 
                        color='white', size=12)
            
            # Print latest values
            print(f"\rAC: {telemetry.ac_current:4.1f}A | "
                  f"DC: {telemetry.dc_current:4.1f}A | "
                  f"Temp: {telemetry.motor_temp:4.1f}°C | "
                  f"Duty: {telemetry.duty_cycle:4.1f}%", end='')
            
        except Exception as e:
            print(f"\nUpdate error: {e}")
        
        return lines.values()

    ani = FuncAnimation(fig, update, interval=5, cache_frame_data=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Starting serial data monitor...")
    print("Press Ctrl+C to exit")
    try:
        create_monitoring_window()
    except KeyboardInterrupt:
        print("\nExiting...")