import serial
import struct
import threading
from collections import deque
from dataclasses import dataclass
import time

@dataclass
class TelemetryData:
    def __init__(self):
        self._lock = threading.Lock()
        # Increase history buffer size for smoother plots
        buffer_size = 1000  # Store 10 seconds of data at 100Hz
        
        # Motor data (ID 0x20)
        self.erpm = 0
        self.duty_cycle = 0
        self.input_voltage = 0
        self.erpm_history = deque(maxlen=buffer_size)
        self.duty_history = deque(maxlen=buffer_size)
        self.voltage_history = deque(maxlen=buffer_size)
        
        # Current data (ID 0x21)
        self.ac_current = 0
        self.dc_current = 0
        self.ac_current_history = deque(maxlen=buffer_size)
        self.dc_current_history = deque(maxlen=buffer_size)
        
        # Temperature data (ID 0x22)
        self.controller_temp = 0
        self.motor_temp = 0
        self.fault_flags = 0
        self.motor_temp_history = deque(maxlen=buffer_size)
        
        self.last_update = {}  # Track last update time for each data type
        self.pps_counter = 0
        self.last_timestamp = time.time()

    def update_pps(self):
        current_time = time.time()
        if current_time - self.last_timestamp >= 1.0:
            self.pps_counter = 0
            self.last_timestamp = current_time
        self.pps_counter += 1

    def update_motor_data(self, timestamp, erpm, duty, voltage):
        with self._lock:
            current_time = time.time()  # Convert to ms
            if 'motor' not in self.last_update or current_time - self.last_update['motor'] >= 10:
                self.erpm = erpm
                self.duty_cycle = duty
                self.input_voltage = voltage
                self.erpm_history.append((timestamp, erpm))
                self.duty_history.append((timestamp, duty))
                self.voltage_history.append((timestamp, voltage))
                self.last_update['motor'] = current_time

    def update_current_data(self, timestamp, ac, dc):
        with self._lock:
            current_time = time.time()  # Convert to ms
            if 'current' not in self.last_update or current_time - self.last_update['current'] >= 10:
                self.ac_current = ac
                self.dc_current = dc
                self.ac_current_history.append((timestamp, ac))
                self.dc_current_history.append((timestamp, dc))
                self.last_update['current'] = current_time

    def update_temp_data(self, timestamp, controller_temp, motor_temp, flags):
        with self._lock:
            self.controller_temp = controller_temp
            self.motor_temp = motor_temp
            self.fault_flags = flags
            self.motor_temp_history.append((timestamp, motor_temp))

    def get_plot_data(self, data_type):
        with self._lock:
            if data_type == 'ac_current':
                data = list(self.ac_current_history)
            elif data_type == 'dc_current':
                data = list(self.dc_current_history)
            elif data_type == 'duty':
                data = list(self.duty_history)
            elif data_type == 'voltage':
                data = list(self.voltage_history)
            elif data_type == 'motor_temp':
                data = list(self.motor_temp_history)
            
            # Return empty lists if no data
            if not data:
                return [], []
                
            # Unzip the data into timestamps and values
            timestamps, values = zip(*data)
            return list(timestamps), list(values)

# Global instance
telemetry = TelemetryData()

def parse_packet(packet_str: str) -> None:
    """Parse hex formatted packet with specific delimiter structure."""
    try:
        # Debug print to see raw packet
        print(f"Raw packet: {packet_str}")
        
        # Split the packet string and handle possible extra spaces
        parts = packet_str.strip().split()
        if len(parts) < 10:  # Minimum parts needed (timestamp + canid + 8 data bytes)
            print(f"Invalid packet length: {len(parts)}")
            return
            
        # First part is timestamp, second is CANID, rest are data bytes
        timestamp = int(parts[0], 16)
        can_id = int(parts[1], 16)
        
        # Convert remaining parts to bytes
        try:
            payload = bytes([int(x, 16) for x in parts[2:10]])  # Take only 8 data bytes
        except ValueError as e:
            print(f"Error converting hex: {e}")
            return

        telemetry.update_pps()
        
        if can_id == 0x2014:  # Motor data
            erpm, duty_cycle, input_voltage = struct.unpack('>ihh', payload[:8])
            telemetry.update_motor_data(
                timestamp, 
                erpm, 
                duty_cycle / 10,  # Scale to percentage
                input_voltage / 10   # Scale to volts
            )
            print(f"Parsed motor data: ERPM={erpm}, Duty={duty_cycle/1000}%, Voltage={input_voltage/10}V")

        elif can_id == 0x2114:  # Current data
            ac_current, dc_current = struct.unpack('>hh', payload[:4])
            telemetry.update_current_data(
                timestamp,
                ac_current / 10,  # Scale to amps
                dc_current / 10   # Scale to amps
            )
            print(f"Parsed current data: AC={ac_current/10}A, DC={dc_current/10}A")

        elif can_id == 0x2214:  # Temperature data
            controller_temp, motor_temp, fault_flags = struct.unpack('>hhB', payload[:5])
            telemetry.update_temp_data(
                timestamp,
                controller_temp / 10,  # Scale to celsius
                motor_temp / 10,       # Scale to celsius
                fault_flags
            )
            print(f"Parsed temp data: Controller={controller_temp/10}°C, Motor={motor_temp/10}°C")

    except Exception as e:
        print(f"Error parsing packet: {e}")
        print(f"Packet contents: {packet_str}")

def start_serial_reader():
    """Read serial data with hex format and specific delimiters."""
    ser = serial.Serial(
        port='COM8',
        baudrate=1152000,
        timeout=0,
        xonxoff=False,
        rtscts=False
    )
    
    ser.reset_input_buffer()
    last_read = time.time()
    
    while True:
        try:
            current_time = time.time()
            if ser.in_waiting and (current_time - last_read) >= 0.01:  # 10ms minimum between reads
                line = ser.readline().decode('utf-8').strip()
                if line:
                    parse_packet(line)
                last_read = current_time
        except Exception as e:
            print(f"Serial Read Error: {e}")
            ser.reset_input_buffer()

# Start serial reading in background thread
serial_thread = threading.Thread(target=start_serial_reader, daemon=True)
serial_thread.start()