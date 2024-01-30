# GSender - GCode Sender with Stop Functionality

This Python script reads a GCode file and sends position commands to stepper drivers over a serial connection. The GCode file is parsed to extract X, Y, and Z positions, which are then sent as formatted strings over the serial port. The script waits for an acknowledgment (0xAA) from the stepper drivers and provides a stop functionality through a keyboard input ('s' or 'S').

## Features

- Parses GCode file to extract X, Y, Z positions.
- Sends position commands to stepper drivers over a serial connection.
- Waits for an acknowledgment (0xAA) from the stepper drivers.
- Provides a stop functionality through keyboard input ('s' or 'S').

## Usage

```bash
python GSender.py <gcode_file> --port <serial_port> [--baudrate <baud_rate>]

