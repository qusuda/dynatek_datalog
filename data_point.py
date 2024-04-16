import struct

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
        #<55_8BIT>
        struct_format = '>BBHHBBBBBBHHBBBBBBBBHB'
        unpacked_data = struct.unpack(struct_format, chunk_data)
        #print(f'TACH: {unpacked_data[3]} R_WHL: {unpacked_data[2]} S4: {unpacked_data[11]} AN1 {unpacked_data[6]} AN2 {unpacked_data[7]} AN3 {unpacked_data[8]} AN4 {unpacked_data[9]}')
        # Assign to members
        self.start_byte_1 = unpacked_data[0]
        self.start_byte_2 = unpacked_data[1]
        if unpacked_data[2] != 0:
            self.rwhl_rpm = int(3000000 / unpacked_data[2])
        else:
            self.rwhl_rpm = 0.0
        if unpacked_data[3] != 0:
            self.tach_rpm = int(3000000 / unpacked_data[3])
        else:
            self.tach_rpm  = 0.0
        self.switch1 = bool(unpacked_data[4] & 4)
        self.switch2 = bool(unpacked_data[4] & 8)
        self.switch3 = bool(unpacked_data[4] & 16)
        self.switch4 = bool(unpacked_data[4] & 32)
        self.battery_voltage = unpacked_data[5] * 60.6 / 1000
        self.ana_ch1 = unpacked_data[6] / 255 * 5.0
        self.ana_ch2 = unpacked_data[7] / 255 * 5.0
        self.ana_ch3 = unpacked_data[8] / 255 * 5.0
        self.ana_ch4 = unpacked_data[9] / 255 * 5.0
        if unpacked_data[10] != 0:
            self.s3_rpm = int(3000000 / unpacked_data[10])
        else:
            self.s3_rpm = 0.0
        self.s4_rpm = unpacked_data[11]
        self.ana_ch12 = unpacked_data[12] / 255 * 5.0
        self.ana_ch11 = unpacked_data[13] / 255 * 5.0
        self.ana_ch10 = unpacked_data[14] / 255 * 5.0
        self.ana_ch9 = unpacked_data[15] / 255 * 5.0
        self.ana_ch8 = unpacked_data[16] / 255 * 5.0
        self.ana_ch7 = unpacked_data[17] / 255 * 5.0
        self.ana_ch6 = unpacked_data[18] / 255 * 5.0
        self.ana_ch5 = unpacked_data[19] / 255 * 5.0
        self.sample_id = unpacked_data[20]
        self.stop_byte_1 = unpacked_data[21]

    def init_from_serial_data(self, chunk_data):
        """ Init data point from raw serial data chunk"""
        struct_format = '>BBHHBBBBBBHHBBBBBBBBHB'
        unpacked_data = struct.unpack(struct_format, chunk_data)
        print(unpacked_data[3])
        # Assign to members
        self.start_byte_1 = unpacked_data[0]
        self.start_byte_2 = unpacked_data[1]
        self.rwhl_rpm = int(300000 / unpacked_data[2]) # RPM
        self.tach_rpm = unpacked_data[3] # RPM
        self.switch1 = bool(unpacked_data[4] & 4)
        self.switch2 = bool(unpacked_data[4] & 8)
        self.switch3 = bool(unpacked_data[4] & 16)
        self.switch4 = bool(unpacked_data[4] & 32)
        self.battery_voltage = unpacked_data[5] * 60.6 # mV
        self.ana_ch1 = unpacked_data[6] # Fuel pressure
        self.ana_ch2 = unpacked_data[7] # G-force
        self.ana_ch3 = unpacked_data[8]
        self.ana_ch4 = unpacked_data[9] # Gas spjeld
        self.s3_rpm = unpacked_data[10]
        self.s4_rpm = unpacked_data[11]
        self.ana_ch12 = unpacked_data[12]
        self.ana_ch11 = unpacked_data[13]
        self.ana_ch10 = unpacked_data[14]
        self.ana_ch9 = unpacked_data[15]
        self.ana_ch8 = unpacked_data[16]
        self.ana_ch7 = unpacked_data[17]
        self.ana_ch6 = unpacked_data[18] # Temperature back
        self.ana_ch5 = unpacked_data[19] # Temperature front
        self.sample_id = unpacked_data[20]
        self.stop_byte_1 = unpacked_data[21]

    def print_live(self):
        """ Print live"""
        print(f'\rTACH: {self.tach_rpm} '
              f'R_WHL: {self.rwhl_rpm} '
              f'S3: {self.s3_rpm} '
              f'S4: {self.s4_rpm} '
              f'AN1: {self.ana_ch1:.2f} '
              f'AN2: {self.ana_ch2:.2f} '
              f'AN3: {self.ana_ch3:.2f} '
              f'AN4: {self.ana_ch4:.2f} '
              f'SW1: {int(self.switch1)} '
              f'SW2: {int(self.switch2)} '
              f'SW3: {int(self.switch3)} '
              f'SW4: {int(self.switch4)} ', end='', flush=True)
    
            #print(f'TACH: {self.tach_rpm:.2f} R_WHL: {self.rwhl_rpm:.2f} S4: {self.s4_rpm:.2f} AN1 {self.ana_ch1:.2f} AN2 {self.ana_ch2:.2f} AN3 {self.ana_ch3:.2f} AN4 {self.ana_ch4:.2f}')
