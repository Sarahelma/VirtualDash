# VirtualDash
A simple modular Tkinter application to display live vehicle telemetry data arriving via serial port. Designed to be used with Manchester Stringer Motorsports electric vehicle

Serial data should print to serial port in hexadecimal in the following format:
```
Timestamp (4 bytes)  CANID(4 bytes)  Data(8 bytes)
eg. 00000000 2014 00 11 22 33 44 55 66 77               
```
## CAN Messages

The following CAN IDs are supported based on the DTI HV500 motor controller:

| CAN ID  | Description                                     |
|---------|-------------------------------------------------|
| 0x2014  | ERPM, Duty, Input Voltage                       |
| 0x2114  | AC Current, DC Current                          |
| 0x2214  | Controller Temp., Motor Temp., Fault code       |
| 0x2314  | Id, Iq values                                   |
| 0x2414  | Throttle signal, Brake signal, Digital I/Os, Drive enable, Limit status bits, CAN map version  |

Additional IDs can be added to the DBC file.
Any additional IDs should be added to the DBC file, to modify the interface to display additiona


This tool was developed with the assistance of Github Co-Pilot Claude 3.5 Sonnet.
