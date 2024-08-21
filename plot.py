"""Module for parsing and plotting data downloaded from Dynatek datalogger"""

#import os
import sys
import matplotlib.pyplot as plt
from data_point import DataPoint
import matplotlib.gridspec as gridspec
import mplcursors

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

    battery_voltage = [data_point.battery_voltage for data_point in data_points]

    tach_rpms = [data_point.tach_rpm for data_point in data_points]
    rwhl_rpms = [data_point.rwhl_rpm for data_point in data_points]
    s3_rpms = [data_point.s3_rpm for data_point in data_points]

    s4_rpms = [data_point.s4_rpm for data_point in data_points]

    fuel_pressure = [data_point.fuel_pressure for data_point in data_points]
    g_force = [data_point.g_force for data_point in data_points]
    throttle = [data_point.throttle for data_point in data_points]
    
    temp_front = [data_point.temperature_front for data_point in data_points]
    temp_back = [data_point.temperature_back for data_point in data_points]

    switch1 = [data_point.switch1 for data_point in data_points]

    #Plot the measurements
    fig = plt.figure()  # Total figure size
    #fig, axis = plt.subplots(5, 1)

    axis = []
    # Create a GridSpec with 3 rows and 1 column
    gs = gridspec.GridSpec(5, 1, height_ratios=[8, 4, 4, 4, 1])  # Adjust height_ratios as needed
    axis.append(fig.add_subplot(gs[0]))
    axis.append(fig.add_subplot(gs[1]))
    axis.append(fig.add_subplot(gs[2]))
    axis.append(fig.add_subplot(gs[3]))
    axis.append(fig.add_subplot(gs[4]))
    #ax2 = fig.add_subplot(gs[1])
    #ax3 = fig.add_subplot(gs[2])
    #ax4 = fig.add_subplot(gs[3])
    #ax5 = fig.add_subplot(gs[4])

    plt.suptitle(f"{event}", y=0.97)

    plot_cnt = 0

    # Set the background color for the figure
    fig.patch.set_facecolor('slategray')

    # axis[plot_cnt].set_ylabel("Voltage", color= "purple")
    # axis[plot_cnt].plot(sample_ids, battey_voltage, color='purple')
    # axis[plot_cnt].get_xaxis().set_visible(False)
    # axis[plot_cnt].set_ylim(10, 14)

    # plot_cnt = plot_cnt + 1
    axis[plot_cnt].set_ylabel("RPM", color= "blue")
    axis[plot_cnt].plot(sample_ids, tach_rpms , color='blue', label='TACH')
    axis[plot_cnt].plot(sample_ids, rwhl_rpms , color='magenta', label='RWHL')
    #axis[plot_cnt].plot(sample_ids, s4_rpms , color='grey', label='S4')
    axis[plot_cnt].plot(sample_ids, s3_rpms , color='red', label='S3')
    #axis[1].plot(sample_ids, s4_rpms , color='cyan', label='Clutch slip')
    axis[plot_cnt].get_xaxis().set_visible(False)
    axis[plot_cnt].set_ylim(0, 8000)
    axis[plot_cnt].legend(loc='upper left', ncol=2)
    #axis[plot_cnt].legend(loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=4) # bbox_to_anchor=(0.5, -0.3)

    plot_cnt = plot_cnt + 1

    axis[plot_cnt].set_ylabel("Exhaust Temp [C]", color= "orange")
    axis[plot_cnt].plot(sample_ids, temp_front , color='red', label='Front')
    axis[plot_cnt].plot(sample_ids, temp_back , color='yellow', label='Back')
    axis[plot_cnt].get_xaxis().set_visible(False)
    axis[plot_cnt].set_ylim(0, 400)
    # Add a legend
    #axis[plot_cnt].legend(loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=2) # bbox_to_anchor=(0.5, -0.3)
    axis[plot_cnt].legend(loc='upper left', ncol=2)
    plot_cnt = plot_cnt + 1

    axis[plot_cnt].set_ylabel("Fuel press.(PSI)", color= "cyan")
    axis[plot_cnt].plot(sample_ids, fuel_pressure , color='cyan', label="Pressure  (PSI)")
    axis[plot_cnt].plot(sample_ids, throttle , color='magenta', label="Throttle")
    axis[plot_cnt].get_xaxis().set_visible(False)
    # Add a legend
    axis[plot_cnt].legend(loc='upper left', ncol=2)
    #axis[plot_cnt].legend(loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=2) # bbox_to_anchor=(0.5, -0.3)
    #axis[plot_cnt].set_ylim(0, 100)

    plot_cnt = plot_cnt + 1

    axis[plot_cnt].set_ylabel("G force", color= "green")
    axis[plot_cnt].plot(sample_ids, g_force , color='green')
    axis[plot_cnt].get_xaxis().set_visible(False)
    axis[plot_cnt].set_ylim(0, 5)

    plot_cnt = plot_cnt + 1

    axis[plot_cnt].set_ylabel("Gear shift", color= "blue")
    axis[plot_cnt].plot(sample_ids, switch1, label='Gear shift')
    axis[plot_cnt].get_xaxis().set_visible(True)
    axis[plot_cnt].get_xaxis().set_label('Time')
    #axis[plot_cnt].legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=4)
    axis[plot_cnt].set_ylim(0, 1.2)
    #axis[plot_cnt].set_height(10)

    for ax in axis:
        ax.set_facecolor('gray')


    plt.subplots_adjust(top=0.939, bottom=0.045, left=0.055, right=0.99, hspace=0.223, wspace=0.2)

    # Make the plot full screen
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    # Add cursors to the plot
    #mplcursors.cursor(hover=True)
    mplcursors.cursor(hover=True, multiple=True)


    #plt.tight_layout()
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
