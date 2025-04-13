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


This tool was developed with the assistance of Github Co-Pilot Claude 3.5 Sonnet.