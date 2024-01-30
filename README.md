# GSender - GCode Sender with Stop Functionality

This Python script reads a GCode file and sends position commands to stepper drivers over a serial connection. The GCode file is parsed to extract X, Y, and Z positions, which are then sent as formatted strings over the serial port. The script waits for an acknowledgment (0xAA) from the stepper drivers and provides a stop functionality through a keyboard input ('s' or 'S').

# Features

- Parses GCode file to extract X, Y, Z positions.
- Sends position commands to stepper drivers over a serial connection.
- Waits for an acknowledgment (0xAA) from the stepper drivers.
- Provides a stop functionality through keyboard input ('s' or 'S').

# Usage

```bash
python GSender.py <gcode_file> --port <serial_port> [--baudrate <baud_rate>]
```

# Arguments

* gcode_file: Path to the GCode file to be processed.
* port: Serial port name (e.g., COM3, /dev/ttyUSB0).
* baudrate: Baud rate for serial communication (default: 9600).

# Getting Started

### Prerequisites

Python 3.x installed
Git installed (optional for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cosmok82/GSender.git
```
or download and extract the ZIP file.

2. Navigate to the project directory:
```bash
cd GSender
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the script with the following command:
```bash
python GSender.py <gcode_file> --port <serial_port> [--baudrate <baud_rate>]
```
Replace <gcode_file>, <serial_port>, and <baud_rate> with your specific values.

### Example

```bash
python GSender.py example.gcode --port COM3 --baudrate 9600
```

# Contributing
Contributions are welcome! Feel free to open issues or pull requests.

# License
This project is licensed under the MIT License - see the LICENSE file for details.


