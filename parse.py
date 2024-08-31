"""Module for parsing and plotting data downloaded from Dynatek datalogger"""

import sys
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
    
def process(data_points):
    for dp in data_points:
        dp.process()

def filter(data_points):
    if len(data_points) < 10:
        return data_points
    
    # Loop through the array starting from the 10th element
    for i in range(9, len(data_points)):
        if (data_points[i].s3_rpm == data_points[i-1].s3_rpm == 
            data_points[i-2].s3_rpm == data_points[i-3].s3_rpm == 
            data_points[i-4].s3_rpm == data_points[i-5].s3_rpm == 
            data_points[i-6].s3_rpm == data_points[i-7].s3_rpm == 
            data_points[i-8].s3_rpm == data_points[i-9].s3_rpm):
            for j in range(i, i-10, -1):
                data_points[j].s3_rpm = 0
    return data_points