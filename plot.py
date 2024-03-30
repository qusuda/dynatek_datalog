"""Module for parsing and plotting data downloaded from Dynatek datalogger"""

#import os
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
        struct_format = '>BBHHBBBBBBHHBBBBBBBBHBB'
        unpacked_data = struct.unpack(struct_format, chunk_data)
        # Assign to members
        self.start_byte_1 = unpacked_data[0]
        self.start_byte_2 = unpacked_data[1]
        self.rwhl_rpm = unpacked_data[2]
        self.tach_rpm = unpacked_data[3]
        self.gpio_pins = unpacked_data[4]
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
        self.stop_byte_2 = unpacked_data[21]
        self.stop_byte_1 = unpacked_data[22]

def parse_file(input_file, chunk_size, offset):
    """Function downloading data"""
    # Open the binary file for reading in binary mode
    with open(input_file, 'rb') as f:
        # Seek to the specified offset
        f.seek(offset)

        # Initialize data point array
        data_points = []
        chunk_number = 0

        while True:
            # Read the chunk
            chunk_data = f.read(chunk_size)
            # Check if chunk is not empty
            if chunk_data:
                data_point = DataPoint(chunk_data)
                data_points.append(data_point)
                # Increment chunk number
                chunk_number += 1
            else:
                # End of file
                break

        # Extracting data members for plotting
        sample_ids = [data_point.sample_id for data_point in data_points]
        rwhl_rpms = [data_point.rwhl_rpm for data_point in data_points]
        ana_ch1s = [data_point.ana_ch1 for data_point in data_points]

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(sample_ids, rwhl_rpms, label='RWHl RPM')
        plt.plot(sample_ids, ana_ch1s, label='ANA CH1')
        plt.xlabel('Sample ID')
        plt.ylabel('Values')
        plt.title('Data Members vs Sample ID')
        plt.legend()
        plt.grid(True)
        plt.show()

    #Plot the measurements
    #fig, ax1 = plt.subplots()
    # fig, ax1 = plt.subplots(figsize=(12, 6))  # Adjust figure size as needed
    # ax1.set_xlabel('Time')
    # ax1.set_ylabel('Analogue value', color='tab:blue')
    # ax1.plot(x_values, y_values[1], color='tab:blue')

    # # Plot other measurements
    # series_count = 0
    # #for i in [2,6,7,8,11,12]:
    # for i in [2,3,4,5,6,7]:
    #    print(f"Add series: {i}")
    #    ax = ax1.twinx()
    #    ax.spines['right'].set_position(('outward', 30 * (series_count)))  # Move the spine to the right
    #    ax.set_ylabel(f'Serie {i}', color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
    #    ax.plot(x_values, y_values[i], color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
    #    ax.set_ylim(310, 430)
    #    series_count = series_count + 1

    # for i in [3,4,15,16,17,18]:
    # #for i in []:
    #    print(f"Add series: {i}")
    #    ax = ax1.twinx()
    #    #ax.spines['right'].set_position(('outward', 30 * (series_count)))  # Move the spine to the right
    #    #ax.set_ylabel(f'Serie {i}', color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan"][i - 1]}')
    #    ax.plot(x_values, y_values[i], color=f'tab:{["blue", "green", "red", "orange", "purple", "pink", "brown", "cyan", "olive", "gray", "red", "orange", "blue", "orange", "pink", "purple", "cyan", "olive"][i - 1]}')
    #    #series_count = series_count + 1

    # plt.subplots_adjust(right=0.95)  # Adjust right margin to make room for spines
    # plt.title(f"{input_file}")
    # plt.tight_layout()  # Adjust layout
    #plt.show()
        
def parse_legacy_file(input_file, chunk_size, offset):
    

if __name__ == "__main__":
    OFFSET = 1178
    CHUNK_SIZE = 38
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> <chunk_size> <offset>")
        sys.exit(1)

    if len(sys.argv) >= 3:
        CHUNK_SIZE = int(sys.argv[2])

    if len(sys.argv) >= 4:
        OFFSET = int(sys.argv[3])

    INPUT_FILE = sys.argv[1]
    print(CHUNK_SIZE)
    print(OFFSET)
    parse_file(INPUT_FILE, CHUNK_SIZE, OFFSET)
