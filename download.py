"""Module for downloading data from Dynatek datalogger"""

import sys
import datetime
import serial
import time

# COM port settings
DEFAULT_COM_PORT = 'COM4'  # Change this to your COM port
BAUD_RATE = 9600


#sim_file = "data/event_2024-04-07_14-12-52_switch_1_2_3_4.log"
#sim_file = "test/input_simulation.log"
sim_file = ""

expected_data_cnt = 62235 
#expected_data_cnt = 62233 

def download(port, event, progress_cb):
    """Function downloading data"""
    ser = None
    sync = None

    # Generate file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f'{event}_{timestamp}.log'

    data_count = 0 

    if len(sim_file) > 0:
        with open(sim_file, 'rb') as infile:
            # Open file for writing binary data
            with open(output_file, 'wb') as file:
                print(f"Writing binary data from {port} to {output_file}...")
                while True:
                    # Read binary data from COM port
                    data = infile.read(1)
                    if data:
                        if data[0] == 0xAA:
                            sync = True
                        if sync:
                            # Write binary data to file
                            file.write(data)
                            file.flush()  # Ensure data is written immediately
                        data_count += 1
                        if progress_cb is not None:
                            progress_cb("Downloading", 100 * data_count // expected_data_cnt)
                    else:
                        break
                    if data_count == expected_data_cnt: ## TODO +2
                        if progress_cb is not None:
                            progress_cb("Done", 100 * data_count // expected_data_cnt)
                        # TODO listen for FFFF sample id
                        return output_file
                    time.sleep(0.0001)
    else:
        try:
            # Open COM port
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            if ser.is_open:
                print(f"Serial port {port} opened successfully.")
            print ("COM port opened")
            # Open file for writing binary data
            with open(output_file, 'wb') as file:
                print(f"Writing binary data from {port} to {output_file}...")
                while True:
                    # Read binary data from COM port
                    data = ser.read(1)
                    #print(data)
                    if data:
                        if data[0] == 0xAA:
                            sync = True
                        if sync:
                            # Write binary data to file
                            file.write(data)
                            file.flush()  # Ensure data is written immediately
                        data_count += 1
                        if progress_cb is not None:
                            progress_cb("Downloading", 100 * data_count // expected_data_cnt)
                    # else:
                    #     break
                    if data_count == expected_data_cnt:
                        if progress_cb is not None:
                            progress_cb("Done", 100 * data_count // expected_data_cnt)
                        # TODO listen for FFFF sample id
                        return output_file
        except serial.SerialException as e:
            print(f"Error: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()
                print(f"Serial port {port} closed.")

    return output_file

if __name__ == "__main__":
    COM_PORT = DEFAULT_COM_PORT
    EVENT_NAME = "event"

    if len(sys.argv) < 3:
        print("Usage: python download.py <COM_port> <event_name>")

    if len(sys.argv) > 2:
        event_name = sys.argv[2]

    if len(sys.argv) > 1:
        COM_PORT = sys.argv[1]

    download(COM_PORT, EVENT_NAME, None)
