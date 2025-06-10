import serial
from serial.threaded import ReaderThread, LineReader
import cantools
import time
from collections import deque
import queue

class SerialReaderProtocolLine(LineReader):
    data_listener = None
    TERMINATOR = b'\n'

    def connection_made(self, transport):
        super().connection_made(transport)
        print("Connected to device")

    def handle_line(self, line):
        if line and self.data_listener:
            self.data_listener.on_data(line.strip())

class DBCProcessor:
    def __init__(self, port="COM8", baud=115200, dbc_path="bms_can_database.dbc"):
        print("Initializing DBC Processor...")
        # Load DBC file
        try:
            self.db = cantools.database.load_file(dbc_path)
            print(f"DBC loaded successfully with {len(self.db.messages)} messages")
        except Exception as e:
            print(f"Failed to load DBC: {e}")
            raise

        # Data storage with buffer
        self.max_points = 3000  # Store 60 seconds at 50Hz
        self.timestamps = {}
        self.values = {}
        
        self.flag_update_queue = queue.Queue()
        

        self.last_pps_time = time.time()
        self.packets_received = 0
        self.packets_per_second = 0
     
        self.inverter_flags = [
            ('DCOV', 0),  # DC OverVoltage 
            ('DCUV', 0),  # DC UnderVoltage
            ('DRV', 0),   # Transistor Drive Error
            ('ACOC', 0),  # AC Over Current
            ('CTRT', 0),  # Controller Temperature
            ('MTRT', 0),  # Motor Temperature
            ('SWF', 0),   # Sensor Wire Fault
            ('SGF', 0),   # Sensor General Fault
            ('CANF', 0)   # CAN Fault
        ]

        self.battery_flags = [
            ('BOV', 1),   # Battery OverVoltage
            ('BUV', 1),   # Battery UnderVoltage
            ('B T', 1),   # Battery Temperature
            ('D OC', 1),  # Discharge OverCurrent
            ('C OC', 1),  # Charge OverCurrent
            ('COM', 1),   # Communication Error
            ('LEAK', 1)   # Leak Fault
        ]
        
        # Moved from data.py
        self.imd_flags = [
            ('GNDF', 1),  # Ground Fault
            ('ERR', 1),   # Error
            ('UV', 1),    # Under Voltage
            ('INSF', 1)   # Insulation Fault
        ]
        
        #Callbacks for flags
        self.flag_callbacks = []  
        self.battery_flag_callbacks = []  
        self.imd_flag_callbacks = [] 
        
        for message in self.db.messages:
            for signal in message.signals:
                signal_name = signal.name
                self.timestamps[signal_name] = deque(maxlen=self.max_points)
                self.values[signal_name] = deque(maxlen=self.max_points)
        
        # Start serial immediately
        try:
            print(f"Connecting to {port} at {baud} baud...")
            self.serial_port = serial.Serial(port, baud, timeout=1)
            SerialReaderProtocolLine.data_listener = self
            self.reader_thread = ReaderThread(self.serial_port, SerialReaderProtocolLine)
            self.reader_thread.start()
            print("Serial connection established")
        except Exception as e:
            print(f"Serial connection failed: {e}")
            raise

        self.expected_interval = 20  # Expected time between samples in ms
        self.last_timestamps = {}    # Track last timestamp per signal
        self.debug_logging = True    # Enable/disable debug logging

    def __del__(self):
        if hasattr(self, 'reader_thread'):
            self.reader_thread.stop()
        if hasattr(self, 'serial_port'):
            self.serial_port.close()

    def on_data(self, data):
        try:
            # Update PPS counter
            self.packets_received += 1
            current_time = time.time()
            if current_time - self.last_pps_time >= 1.0:
                self.packets_per_second = self.packets_received
                self.packets_received = 0
                self.last_pps_time = current_time
            
            # Process CAN data
            parts = data.split()
            if len(parts) < 3:
                return

            timestamp = int(parts[0], 16)  # Using timestamp from message
            can_id = int(parts[1], 16)
            
            try:
                message = self.db.get_message_by_frame_id(can_id)
                if not message:
                    available_ids = [msg.frame_id for msg in self.db.messages[:5]]  # First 5
                    print(f"No message found for CAN ID: 0x{can_id:08X}")
                    print(f"Available message IDs: {[hex(id) for id in available_ids]}")
                    return

                data_bytes = bytes([int(b, 16) for b in parts[2:]])
                
                decoded = message.decode(data_bytes)
            
                if 'Actual_FaultCode' in decoded:
                    fault_code = int(decoded['Actual_FaultCode'])
                    self.flag_update_queue.put(("inverter", fault_code))
    
                for signal_name, value in decoded.items():
                    validated_timestamp = self.validate_timestamp(signal_name, timestamp)
                    self.timestamps[signal_name].append(validated_timestamp)
                    self.values[signal_name].append(value)
                    
            except cantools.database.errors.DecodeError:
                pass
                
        except Exception as e:
            print(f"Data parsing error: {e}")

    def update_inverter_flags(self, fault_code):
        for i in range(len(self.inverter_flags)):
            self.inverter_flags[i] = (self.inverter_flags[i][0], 0)
        
        # Set flags based on fault code
        if fault_code != 0:  
            if 1 <= fault_code <= len(self.inverter_flags):
                # Set the specific flag
                flag_name, _ = self.inverter_flags[fault_code-1]  # Adjust for 0-indexing
                self.inverter_flags[fault_code-1] = (flag_name, 1)
    
    def process_flag_updates(self, root):
        try:
            while not self.flag_update_queue.empty():
                flag_type, code = self.flag_update_queue.get_nowait()
                
                if flag_type == "inverter":
                    self.update_inverter_flags(code)
                    for callback in self.flag_callbacks:
                        callback(self.inverter_flags)
            root.after(100, self.process_flag_updates, root)
        except Exception as e:
            print(f"Error processing flag updates: {e}")
            root.after(100, self.process_flag_updates, root)
    
    def register_flag_callback(self, callback):
        self.flag_callbacks.append(callback)
    
    def get_inverter_flags(self):
        return self.inverter_flags
        
    def update_battery_flags(self, flags_byte):
        pass

    def update_imd_flags(self, flags_byte):
        pass

    def register_battery_flag_callback(self, callback):
        self.battery_flag_callbacks.append(callback)

    def register_imd_flag_callback(self, callback):
        self.imd_flag_callbacks.append(callback)
    
    def get_signal_data(self, signal_name):
        if signal_name in self.timestamps:
            return list(self.timestamps[signal_name]), list(self.values[signal_name])
        return [], []
    
    def get_pps(self):
        return self.packets_per_second

    def validate_timestamp(self, signal_name, new_timestamp):
        if signal_name not in self.last_timestamps:
            self.last_timestamps[signal_name] = new_timestamp
            return new_timestamp
        
        time_diff = new_timestamp - self.last_timestamps[signal_name]
        
        if time_diff > 1000:  # Gap larger than 1 second
            if self.debug_logging:
                print(f"Large timestamp gap detected: {time_diff}ms for {signal_name}")
            # Use expected interval instead
            new_timestamp = self.last_timestamps[signal_name] + self.expected_interval
        
        self.last_timestamps[signal_name] = new_timestamp
        return new_timestamp