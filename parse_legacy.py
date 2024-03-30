"""Module for parsing and plotting legacy data file downloaded using old software"""
# import os
import sys
import struct
import matplotlib.pyplot as plt

class DataPoint:
    """Class representing datalogger data point"""
    def __init__(self, chunk_data):
        # Define the C struct format string corresponding to the struct layout
        #<AA_8BIT><UNKNOWN_8BIT>
        #<R_WHEEL_RPM_16_BIT><TACH_RPM_16_BIT>
        #<DIGITAL_8BIT><BATT_VOLTAGE_8BIT>
        #<ANA_CH1_8BIT><ANA_CH2_8BIT><ANA_CH3_8BIT><ANA_CH4_8BIT>
        #<S3_RPM_16_BIT><S4_RPM_16_BIT>
        #<AUX_2_ANA_CH12_8BIT><AUX_2_ANA_CH11_8BIT><AUX_2_ANA_CH10_8BIT><AUX_2_ANA_CH9_8BIT>
        #<AUX_1_ANA_CH8_8BIT><AUX_1_ANA_CH7_8BIT><AUX_1_ANA_CH6_8BIT><AUX_1_ANA_CH5_8BIT>
        #<SAMPLE_ID_16_BIT>
        #<UNKNOWN_8BIT><55_8BIT>
        struct_format = '>HHHHHHHHHHHHHHHHHHH'
        unpacked_data = struct.unpack(struct_format, chunk_data)
        # Assign to members
        self.start_byte_1 = 0
        self.start_byte_2 = 0
        self.rwhl_rpm = unpacked_data[1]
        self.tach_rpm = unpacked_data[2]
        self.gpio_pins = unpacked_data[3]
        self.battery_voltage = unpacked_data[5]
        self.ana_ch1 = unpacked_data[6]
        self.ana_ch2 = unpacked_data[7]
        self.ana_ch3 = unpacked_data[8]
        self.ana_ch4 = unpacked_data[9]
        self.s3_rpm = unpacked_data[10]
        self.s3_rpm = unpacked_data[11]
        self.ana_ch12 = unpacked_data[12]
        self.ana_ch11 = unpacked_data[13]
        self.ana_ch10 = unpacked_data[14]
        self.ana_ch9 = unpacked_data[15]
        self.ana_ch8 = unpacked_data[16]
        self.ana_ch7 = unpacked_data[17]
        self.ana_ch6 = unpacked_data[18]
        self.ana_ch5 = unpacked_data[19]
        self.sample_id = unpacked_data[20]
        self.stop_byte_2 = 0 #unpacked_data[21]
        self.stop_byte_1 = 0 #unpacked_data[22]

def read_until_null_termination(file):
    """Read until NULL termination found"""
    buffer_size = 1000   # Adjust buffer size according to your needs
    buffer = b''  # Initialize an empty buffer for storing read bytes
    while True:
        chunk = file.read(buffer_size)  # Read a chunk of bytes
        if not chunk:  # End of file reached
            break
        buffer += chunk  # Append the read bytes to the buffer
        if b'\x00' in chunk:  # Check if null termination is in the chunk
            break
    # Decode bytes to ASCII string, ignoring decoding errors
    return buffer.decode('cp865', errors='ignore')  


def parse_legacy_file(input_file, chunk_size, offset):
    """Parse legacy file"""
    # Open the binary file for reading in binary mode
    with open(input_file, 'rb') as f:
        event_desc = read_until_null_termination(f)
        print(event_desc)
        # Seek to the specified offset
        f.seek(offset)

        # Initialize chunk counter and y-values dictionary
        chunk_number = 1
        x_values = []  # Store x values (first word in each chunk)
        # Dictionary to store y values for each measurement
        y_values = {i: [] for i in range(1, 19 )}

        print(y_values)

        offset = [0,10000,14766,0,0,0,100,500,9.12,0,0,500,500,0,0,0,0,0,0,0,0,0]
        gain = [1,-15,-29.89,-1,-1,-1,-0.0238,-1,-0.0202,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        label = ["Time","R-Wheel","TACH","Gear","S4","5","C-Slip", "F-Press","G-force","1","1","Temp-F","Temp-B","1","1","1","1","1","1"]

        while True:
            # Read the chunk
            chunk_data = f.read(chunk_size)
            # Check if chunk is not empty
            if chunk_data:
                # Parse the chunk into 2-byte words
                words = [chunk_data[i:i+2] for i in range(0, len(chunk_data), 2)]
                hex_array = ' '.join([format(int.from_bytes(word, 'little'), '04x') for word in words])

                print(f"Chunk {chunk_number}: [{hex_array}]")

                # Extract first word as x value
                x_value = int.from_bytes(words[0], 'little')
                #bin_value = int.from_bytes(words[3], 'big')
                #binary_number = bin(bin_value)
                #print("0b{:016b}".format(bin_value))
                #print(binary_number)
                if x_value:
                    x_values.append(x_value)  # Append x value

                    # Extract y values for each measurement
                    for i, word in enumerate(words[1:], start=1):
                        #value = (max_value[i] - int.from_bytes(word, 'little')) * gain[i] + offset[i]
                        value = int.from_bytes(word, 'little') * gain[i] + offset[i]
                        #value = value / scale[i]
                        #y_values[i].append(((gain[i] * int.from_bytes(word, 'little')) + offset[i])/scale[i])
                        y_values[i].append(value)

                # Increment chunk number
                chunk_number += 1
            else:
                # End of file
                break

    #Plot the measurements
    #fig, ax1 = plt.subplots()
            

    for i in range(len(y_values[3])):
        if int(y_values[3][i]) & 0x04:  # Checking if the third bit is set
            y_values[3][i] = 1  # Modifying the value to 1 if the bit is set
        else:
            y_values[3][i] = 0  # Modifying the value to 0 if the bit is not set
    
    # Initialise the subplot function using number of rows and columns 
    fig, axis = plt.subplots(8, 1)

    #fig, ax1 = plt.subplots(figsize=(12, 6))  # Adjust figure size as needed
    # axis[0].set_xlabel('Time')
    # axis[0].set_ylabel(label[1], color='tab:blue')
    # axis[0].plot(x_values, y_values[1], color='tab:blue')


    # Plot other measurements
    series_count = 0
    #for i in [2,6,7,8,11,12]:
    for i in [1,2, 3, 6,7,8,11,12]:
        min_val = min(y_values[i])
        max_val = max(y_values[i])
        print(f"Add series ({i})" + label[i])
        print(min_val)
        print(max_val)
        #ax = axis[0].twinx()
        #ax = axis[series_count].twinx()
        #ax = axis[series_count]
         # Move the spine to the right
        #ax.spines['right'].set_position(('outward', 30 * (series_count)))
        axis[series_count].set_ylabel(f' {label[i]}({i})', color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
        axis[series_count].plot(x_values, y_values[i], color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
        #axis[series_count].set_ylim(min_val*0.8, max_val*1.2)
        axis[series_count].get_xaxis().set_visible(False)
        series_count = series_count + 1
    
    axis[series_count-1].get_xaxis().set_visible(True)
    ## The channel below seems unused ( little measure on 4 (39,3a,3b))
    # for i in [4,5,14,15,16,17,18]:
    #    print(f"Add series: {i}")
    #    ax = ax1.twinx()
    #    #ax.spines['right'].set_position(('outward', 30 * (series_count)))  # Move the spine to the right
    #    #ax.set_ylabel(f'Serie {i}', color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
    #    ax.plot(x_values, y_values[i], color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan", "olive"][i - 1]}')
    #    #series_count = series_count + 1

    # plt.subplots_adjust(right=0.95)  # Adjust right margin to make room for spines
    first_line = event_desc.splitlines()[0]
    plt.title(f"{first_line}", y=10.0)
    #plt.suptitle(f"{first_line}", x=0.5, y=1.0, horizontalalignment='center')

    #plt.tight_layout()  # Adjust layout
    plt.show()

if __name__ == "__main__":

    OFFSET = 1178
    CHUNK_SIZE = 38
    if len(sys.argv) < 2:
        print("Usage: python parse_legacy.py <input_file> <chunk_size> <offset>")
        sys.exit(1)

    if len(sys.argv) >= 3:
        CHUNK_SIZE = int(sys.argv[2])

    if len(sys.argv) >= 4:
        OFFSET = int(sys.argv[3])

    INPUT_FILE = sys.argv[1]
    # print(CHUNK_SIZE)
    # print(offset)
    parse_legacy_file(INPUT_FILE, CHUNK_SIZE, OFFSET)
