import serial
from serial.threaded import ReaderThread, LineReader
import time
from collections import deque

# Handles line reading from serial port
class SerialReaderProtocolLine(LineReader):
    data_listener = None
    TERMINATOR = b'\n'

    def connection_made(self, transport):
        super().connection_made(transport)
        print("Connected to device")

    def handle_line(self, line):
        if line and self.data_listener:
            receive_time = int(time.time() * 1000)
            self.data_listener.on_data(line.strip(), receive_time)

class CANDataProcessor:
    def __init__(self, port="COM8", baud=115200):
        # Data storage with fixed buffer size
        self.max_points = 1000
        self.timestamps = {}
        self.values = {}
        
        # Signals defined based on CAN ID, add signals here
        self.signals = {
            0x2014: ['erpm', 'duty_cycle', 'input_volts'],
            0x2114: ['ac_current', 'dc_current'],
            0x2214: ['ctrl_temp', 'motor_temp', 'error_code']
        }
        
        # Initialize storage for each signal
        for can_id, signals in self.signals.items():
            for signal in signals:
                self.timestamps[signal] = deque(maxlen=self.max_points)
                self.values[signal] = deque(maxlen=self.max_points)
        
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

    def __del__(self):
        if hasattr(self, 'reader_thread'):
            self.reader_thread.stop()
        if hasattr(self, 'serial_port'):
            self.serial_port.close()

    def on_data(self, data, receive_time):
        try:
            parsed_data = self.parse_data(data)
            if parsed_data and 'can_id' in parsed_data:
                can_id = parsed_data['can_id']
                if can_id in self.signals:
                    for signal in self.signals[can_id]:
                        if signal in parsed_data:
                            # Store absolute timestamps
                            self.timestamps[signal].append(receive_time)
                            self.values[signal].append(parsed_data[signal])
        except Exception as e:
            print(f"Data parsing error: {e}")

    def parse_data(self, data):
# delimitter is space so split based on space
        parts = data.split()
        if len(parts) < 3:
            return None
            
        try:
            can_id = int(parts[1], 16)
            data_bytes = [int(byte, 16) for byte in parts[2:]]
            result = {"can_id": can_id}
            
            if can_id == 0x2014 and len(data_bytes) >= 8:
                result.update({
                    "erpm": self._bytes_to_signed_int(data_bytes[0:4], 4),
                    "duty_cycle": self._bytes_to_signed_int(data_bytes[4:6], 2) / 10.0,
                    "input_volts": self._bytes_to_signed_int(data_bytes[6:8], 2) / 10.0
                })
            elif can_id == 0x2114 and len(data_bytes) >= 4:
                result.update({
                    "ac_current": self._bytes_to_signed_int(data_bytes[0:2], 2) / 10.0,
                    "dc_current": self._bytes_to_signed_int(data_bytes[2:4], 2) / 10.0
                })
            elif can_id == 0x2214 and len(data_bytes) >= 5:
                result.update({
                    "ctrl_temp": self._bytes_to_signed_int(data_bytes[0:2], 2) / 10.0,
                    "motor_temp": self._bytes_to_signed_int(data_bytes[2:4], 2) / 10.0,
                    "error_code": data_bytes[4]
                })
            return result
            
        except Exception as e:
            print(f"Parse error: {e}")
            return None

    def _bytes_to_signed_int(self, bytes_list, num_bytes):
        value = 0
        for i, byte in enumerate(bytes_list):
            value |= (byte << (8 * i))
        if value & (1 << (num_bytes * 8 - 1)):
            value -= (1 << (num_bytes * 8))
        return value

    def get_signal_data(self, signal):
        if signal in self.timestamps:
            return list(self.timestamps[signal]), list(self.values[signal])
        return [], []

