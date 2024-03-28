"""Module for downloading data from Dynatek datalogger"""

import sys
import datetime
import serial

# COM port settings
DEFAULT_COM_PORT = 'COM1'  # Change this to your COM port
BAUD_RATE = 9600

def download(port, event):
    """Function downloading data"""
    ser = None
    try:
        # Open COM port
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        if ser.is_open:
            print(f"Serial port {port} opened successfully.")

        # Generate file name with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f'{event}_{timestamp}.log'

        # Open file for writing binary data
        with open(output_file, 'wb') as file:
            print(f"Writing binary data from {port} to {output_file}...")
            while True:
                # Read binary data from COM port
                data = ser.read(1)
                if data:
                    # Write binary data to file
                    file.write(data)
                    file.flush()  # Ensure data is written immediately
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"Serial port {port} closed.")

if __name__ == "__main__":
    COM_PORT = DEFAULT_COM_PORT
    EVENT_NAME = "event"

    if len(sys.argv) < 3:
        print("Usage: python download.py <COM_port> <event_name>")

    if len(sys.argv) > 2:
        event_name = sys.argv[2]

    if len(sys.argv) > 1:
        COM_PORT = sys.argv[1]

    download(COM_PORT, EVENT_NAME)
