# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 21:18:51 2024

@author: Cosimo Orlando
"""

"""
GCode Sender with Stop Functionality

This Python script reads a GCode file and sends position commands to stepper drivers over a serial connection. The GCode file is parsed to extract X, Y, and Z positions, which are then sent as formatted strings over the serial port. The script waits for an acknowledgment (0xAA) from the stepper drivers and provides a stop functionality through a keyboard input ('s' or 'S').

Features:
- Parses GCode file to extract X, Y, Z positions.
- Sends position commands to stepper drivers over a serial connection.
- Waits for an acknowledgment (0xAA) from the stepper drivers.
- Provides a stop functionality through keyboard input ('s' or 'S').

Usage:
python gcode_sender.py <gcode_file> --port <serial_port> [--baudrate <baud_rate>]

Arguments:
- gcode_file: Path to the GCode file to be processed.
- port: Serial port name (e.g., COM3, /dev/ttyUSB0).
- baudrate: Baud rate for serial communication (default: 9600).
"""

import argparse
import asyncio
import serial
import re
import time

# Scaling factor for converting floats to unsigned integers
SCALE_FACTOR = 1000

# Global variable to signal a stop request
stop_requested = False

def parse_gcode_line(line):
    """
    Parse a GCode line and extract position information.

    Args:
        line (str): GCode line.

    Returns:
        Tuple or None: Extracted X, Y, Z positions if found, otherwise None.
    """
    match = re.match(r'^G0|G1 X([-+]?\d*\.\d+|\d+) Y([-+]?\d*\.\d+|\d+) Z([-+]?\d*\.\d+|\d+)', line)
    if match:
        x = int(float(match.group(1)) * SCALE_FACTOR)
        y = int(float(match.group(2)) * SCALE_FACTOR)
        z = int(float(match.group(3)) * SCALE_FACTOR)
        return x, y, z
    else:
        return None

async def send_position(serial_port, x, y, z):
    """
    Send position commands to stepper drivers over serial and wait for ACK.

    Args:
        serial_port (serial.Serial): Serial port object.
        x (int): X position.
        y (int): Y position.
        z (int): Z position.
    """
    global stop_requested

    x_sign = 'P' if x >= 0 else 'N'
    y_sign = 'P' if y >= 0 else 'N'
    z_sign = 'P' if z >= 0 else 'N'

    x = abs(x)
    y = abs(y)
    z = abs(z)

    position_string = f"{x_sign}:{x},{y_sign}:{y},{z_sign}:{z}\n"
    serial_port.write(position_string.encode())
    print(f"Sent position: {x_sign}X={x/SCALE_FACTOR}, {y_sign}Y={y/SCALE_FACTOR}, {z_sign}Z={z/SCALE_FACTOR}")

    # Wait for ACK response (0xAA) or check for stop button
    ack_received = False
    timeout = time.time() + 5  # Timeout in seconds
    while not ack_received and time.time() < timeout and not stop_requested:
        response = serial_port.read(1)
        if response == b'\xAA':
            ack_received = True
        await asyncio.sleep(0.1)

    if not ack_received:
        print("Error: ACK (0xAA) not received. Check the connection or adjust timeout.")
        raise asyncio.CancelledError

async def stop_handler():
    """
    Handle keyboard input for stopping the operation.
    """
    global stop_requested
    while True:
        user_input = input("Press 's' or 'S' to stop: ")
        if user_input.lower() == 's':
            stop_requested = True
            print("Stop requested.")
            break

async def main(args):
    """
    Main function to send GCode positions to stepper drivers over serial.

    Args:
        args (argparse.Namespace): Command line arguments.
    """
    global stop_requested  # Explicitly define the global variable

    # Create a serial connection
    serial_port = serial.Serial(args.port, baudrate=args.baudrate, timeout=1)

    try:
        # Start the stop handler in the background
        asyncio.create_task(stop_handler())

        with open(args.gcode_file, 'r') as gcode_file:
            for line in gcode_file:
                position = parse_gcode_line(line)
                if position:
                    await send_position(serial_port, *position)
                    await asyncio.sleep(0.5)  # Adjust delay between commands as needed

                if stop_requested:
                    print("Operation stopped.")
                    break

    finally:
        stop_requested = True  # Stop the handler
        serial_port.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send GCode positions to stepper drivers over serial")
    parser.add_argument("gcode_file", help="Path to the GCode file")
    parser.add_argument("--port", help="Serial port name (e.g., COM3, /dev/ttyUSB0)", required=True)
    parser.add_argument("--baudrate", type=int, help="Baud rate for serial communication", default=9600)

    args = parser.parse_args()

    asyncio.run(main(args))


