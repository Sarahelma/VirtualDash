# VirtualDash
A simple modular Tkinter application to display live vehicle telemetry data arriving via serial port. Designed to be used with Manchester Stringer Motorsports electric vehicle

Serial data should print to serial port in hexadecimal in the following format:

Timestamp (4 bytes)  CANID(4 bytes)  Data(8 bytes)
eg. 00000000  2014  00 11 22 33 44 55 66 77

The following ID's have been incorparated and parsed based on DTI HV500 motor controller:
0x2014
0x2114
0x2214
0x2314

Any additional IDs should be added to the DBC file, to modify the interface to display additiona


## References and Libraries:
This project uses the following libraries:
- [Matplotlib](https://matplotlib.org/) - For data visualization and custom UI elements
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - For GUI implementation
- [cantools](https://github.com/cantools/cantools) - For CAN DBC file parsing
- [pyserial](https://github.com/pyserial/pyserial) - For serial communication
- [tkdial](https://github.com/Akascape/tkdial) - For analog gauges


Disclaimer:
This tool was developed with the assistance of Github Co-Pilot Claude 3.5 Sonnet and later Claude 3.7 Sonnet by Anthropic. Github Copilot was used to generate code, debug errors, integrate working examples into the program, suggest changes and auto-complete lines. 