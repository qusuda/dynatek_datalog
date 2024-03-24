import serial
import sys

# COM port settings
DEFAULT_COM_PORT = 'COM1'  # Change this to your COM port
BAUD_RATE = 9600

def main(com_port, event):
    ser = None
    try:
        # Open COM port
        ser = serial.Serial(com_port, BAUD_RATE, timeout=1)
        if ser.is_open:
            print(f"Serial port {com_port} opened successfully.")

        # Generate file name with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        OUTPUT_FILE = f'{event}_{timestamp}.log'

        # Open file for writing binary data
        with open(OUTPUT_FILE, 'wb') as file:
            print(f"Writing binary data from {com_port} to {OUTPUT_FILE}...")
            while True:
                # Read binary data from COM port
                data = ser.read(1)
                if data:
                    # Write binary data to file
                    file.write(data)
                    file.flush()  # Ensure data is written immediately

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"Serial port {com_port} closed.")

if __name__ == "__main__":
    com_port = DEFAULT_COM_PORT
    event = "event"

    if len(sys.argv) < 3:
        print("Usage: python download.py <COM_port> <event_name>")
    
    if len(sys.argv) > 2:
        event = sys.argv[2]

    if len(sys.argv) > 1:
        com_port = sys.argv[1]
    
    main(com_port, event)