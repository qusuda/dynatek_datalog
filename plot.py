"""Module for parsing and plotting data downloaded from Dynatek datalogger"""

#import os
import sys
import matplotlib.pyplot as plt
from data_point import DataPoint

def parse_file(input_file, chunk_size, offset):
    """Function parsing data file"""
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
            #print(chunk_data.hex())
            # Check if chunk is not empty
            if chunk_data and len(chunk_data) == chunk_size:
                if chunk_data[0] == 0xAA:
                    data_point = DataPoint(chunk_data)
                    data_points.append(data_point)
                    # Increment chunk number
                    chunk_number += 1
            else:
                # End of file
                break

        return data_points 

def plot(data_points, event):
    """Function plotting data points"""
    # Extracting data members for plotting
    sample_ids = [data_point.sample_id for data_point in data_points]

    battey_voltage = [data_point.battery_voltage for data_point in data_points]

    tach_rpms = [data_point.tach_rpm for data_point in data_points]
    rwhl_rpms = [data_point.rwhl_rpm for data_point in data_points]
    s4_rpms = [data_point.s4_rpm for data_point in data_points]

    ana_ch1 = [data_point.ana_ch1 for data_point in data_points]
    ana_ch2 = [data_point.ana_ch2 for data_point in data_points]
    ana_ch4 = [data_point.ana_ch4 for data_point in data_points]
    
    ana_ch5 = [data_point.ana_ch5 for data_point in data_points]
    ana_ch6 = [data_point.ana_ch6 for data_point in data_points]

    switch1 = [data_point.switch1 for data_point in data_points]
    switch2 = [data_point.switch2 for data_point in data_points]
    switch3 = [data_point.switch3 for data_point in data_points]
    switch4 = [data_point.switch4 for data_point in data_points]


    #Plot the measurements
    fig, axis = plt.subplots(6, 1)
    plt.suptitle(f"{event}", y=0.95)

    axis[0].set_ylabel("Voltage", color= "purple")
    axis[0].plot(sample_ids, battey_voltage, color='purple')
    axis[0].get_xaxis().set_visible(False)
    axis[0].set_ylim(10, 14)

    axis[1].set_ylabel("RPM", color= "blue")
    axis[1].plot(sample_ids, tach_rpms , color='blue', label='TACH')
    axis[1].plot(sample_ids, rwhl_rpms , color='magenta', label='RWHL')
    axis[1].plot(sample_ids, s4_rpms , color='grey', label='S4')
    #axis[1].plot(sample_ids, s4_rpms , color='cyan', label='Clutch slip')
    axis[1].get_xaxis().set_visible(False)
    axis[1].set_ylim(0, 8000)
    axis[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=4) # bbox_to_anchor=(0.5, -0.3)

    axis[2].set_ylabel("Temperature [C]", color= "orange")
    axis[2].plot(sample_ids, ana_ch5 , color='red', label='Front')
    axis[2].plot(sample_ids, ana_ch6 , color='yellow', label='Back')
    axis[2].get_xaxis().set_visible(False)
    axis[2].set_ylim(0, 400)
    # Add a legend
    axis[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=2) # bbox_to_anchor=(0.5, -0.3)

    axis[3].set_ylabel("Fuel pressure", color= "cyan")
    axis[3].plot(sample_ids, ana_ch1 , color='cyan')
    axis[3].plot(sample_ids, ana_ch4 , color='magenta')
    axis[3].get_xaxis().set_visible(False)
    axis[3].set_ylim(0, 400)

    axis[4].set_ylabel("G force", color= "green")
    axis[4].plot(sample_ids, ana_ch2 , color='green')
    axis[4].get_xaxis().set_visible(False)
    axis[4].set_ylim(0, 400)

    axis[5].set_ylabel("Switch", color= "blue")
    axis[5].plot(sample_ids, switch1, label='SWITCH 1')
    axis[5].plot(sample_ids, switch2, label='SWITCH 2')
    axis[5].plot(sample_ids, switch3, label='SWITCH 3')
    axis[5].plot(sample_ids, switch4, label='SWITCH 4')
    axis[5].get_xaxis().set_visible(True)
    axis[5].get_xaxis().set_label('Time')
    axis[5].legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=4)
    axis[5].set_ylim(0, 1)   


    plt.subplots_adjust(hspace=0.5)
    #plt.tight_layout(pad=0.5)
    #plt.grid(True)
    plt.show()

    # plt.subplots_adjust(right=0.95)  # Adjust right margin to make room for spines
    # plt.title(f"{input_file}")
    # plt.tight_layout()  # Adjust layout

if __name__ == "__main__":
    OFFSET = 27
    CHUNK_SIZE = 27
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
