"""Module for live data from Dynatek datalogger"""

import sys
import serial
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel

from data_point import DataPoint

# COM port settings
DEFAULT_COM_PORT = 'COM4'  # Change this to your COM port
BAUD_RATE = 9600


#sim_file = "data/event_2024-04-07_14-12-52_switch_1_2_3_4.log"
sim_file = ""

def live(port):
    """Function downloading data"""
    ser = None
    sync = None

    chunk_bytes = bytearray()

    if len(sim_file) > 0:
        with open(sim_file, 'rb') as infile:
            print(f"Reading binary data from {port} to {sim_file}...")
            while True:
                # Read binary data from COM port
                data = infile.read(1)
                if data:
                    if data[0] == 0xAA:
                        sync = True
                    if sync:
                        # Write binary data to file
                        chunk_bytes.extend(data)
                        if len(chunk_bytes) == 27:
                            data_point = DataPoint(chunk_bytes)
                            chunk_bytes.clear()
                            sync = False
                            if data_point:
                                data_point.print_live()
                else:
                    break
                time.sleep(0.0001)
    else:
        try:
            # Open COM port
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            if ser.is_open:
                print(f"Serial port {port} opened successfully.")
            print ("COM port opened")
            while True:
                # Read binary data from COM port
                data = ser.read(1)
                if data:
                    if data[0] == 0xAA:
                        sync = True
                    if sync:
                        # Write binary data to file
                        chunk_bytes.extend(data)
                        if len(chunk_bytes) == 27:
                            data_point = DataPoint(chunk_bytes)
                            chunk_bytes.clear()
                            sync = False
                            if data_point:
                                data_point.print_live()
                # else:
                #     break
        except serial.SerialException as e:
            print(f"Error: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()
                print(f"Serial port {port} closed.")

class LiveApp(QMainWindow):
    def __init__(self, com_port):
        super().__init__()

        self.com_port = com_port

        # Set the window title
        self.setWindowTitle('Dynatek Datalogger - Plot')

        # Create a QWidget for the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout instance
        self.layout = QVBoxLayout(self.central_widget)

        # Event label
        self.event_label = QLabel('Event')
        self.layout.addWidget(self.event_label)

    def start(self):
        live(self.com_port)
        # TODO dethread and visualize Live data

if __name__ == "__main__":
    COM_PORT = DEFAULT_COM_PORT
    EVENT_NAME = "event"

    if len(sys.argv) < 2:
        print("Usage: python live.py <COM_port>")

    if len(sys.argv) > 1:
        COM_PORT = sys.argv[1]

    live(COM_PORT)
