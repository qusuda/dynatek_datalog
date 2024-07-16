# Dynatek Datalog
Python scripts to download and plot data from Dynatek Datalogger

Scripts are made by reverse engineering the communication interface and connected sensors.



## Serial data frame format:

<AA_8BIT><UNKNOWN_8BIT><R_WHEEL_RPM_16_BIT><TACH_RPM_16_BIT><DIGITAL_8BIT><BATT_VOLTAGE_8BIT><ANA_CH1_8BIT><ANA_CH2_8BIT><ANA_CH3_8BIT><ANA_CH4_8BIT><S3_RPM_16_BIT><S4_RPM_16_BIT>
<AUX_2_ANA_CH12_8BIT><AUX_2_ANA_CH11_8BIT><AUX_2_ANA_CH10_8BIT><AUX_2_ANA_CH9_8BIT><AUX_2_ANA_CH8_8BIT><AUX_2_ANA_CH7_8BIT><AUX_2_ANA_CH6_8BIT><AUX_2_ANA_CH5_8BIT><SAMPLE_ID_16_BIT><UNKNOWN_8BIT><55_8BIT>


### Digital 8 bit channels
<0><0><SW_4><SW_3><SW_2><SW_1><0><0><0><0>


## RPM measurement (R_WHEEL / TACH/ S3)

R_WHEEL is backside of gearbox

TACH is crankshaft aka. engine RPM

S3 Not in use in current setup


| RPM  | Hz  | HEX   | Decimal |
|------|-----|-------|---------|
| 100  | 3.3 | 0x7512|  29970  | 
| 200  | 6.6 | 0x3B13|  15123  | 
| 300  | 10  |       |         | 
| 500  | 20  |       |         | 
|1000  | 33.3| 0xB6E |   2926  | 
|2000  | 66.6| 0x5D9 |   1497  | 
|4000  | 133 | 0x2ED |    749  | 
|5000  | 166 |       |         | 
|8000  | 267 | 0x174 |    372  | 
|10000 | 333 |       |         | 

rpm = 300000 / x

## S4 RPM 
This channel different from the other RPM channel
Where TACH, R_WHL and S3 values are based on measuring time between magnets passing the sensor,
values from this sensor is based on frequency


 thersis reversed (higher frequency/RPM -> higher hex value)

S4 is front of clutch  

| RPM  | Hz  | HEX    | Decimal |
|------|-----|--------|---------|
|2000  | 66.6| 0x7E4  |   2020  |
|4000  | 133 | 0xF9E  |   3998  |
|8000  | 267 | 0x1F71 |   8049  |

S4 new measurements

| RPM  |  Hz   |  HEX   | Decimal |
|------|-------|--------|---------|
| 500  | 200   | 
| 1000 | 100   |
| 1500 |  66   |
| 2000 |  50   |
| 2500 |  40   |
| 3000 |  33   |
| 3500 |  28   |
| 4000 |  25   |
| 4500 |  22,3 |
| 5000 |  20   |
| 5500 |  18   |
| 6000 |  16,6 |
| 7000 |  14   |



## Battery voltage

| Voltage | HEX  | Decimal |
|---------|------|---------|
| 10      | 0xA5 | 165     |
| 12      | 0xC6 | 198     |
| 14      | 0xE7 | 231     |


## Analog channels

Analog channels are based on 8-bit ADC 

Input i 0-5V and resulting values are between 0 and 255
| Voltage | HEX  | Decimal |
|---------|------|---------|
| 0       | 0x?? | 0       |
| 1       | 0x?? | ~ 50    |
| 2       | 0x?? | ~ 100   |
| 3       | 0x?? | ~ 154   |
| 4       | 0x?? | ~ 205   |
| 5       | 0x?? | ~ 255   |

value =  input_voltage /  (5V / 255)  
value = input_voltage * 255 / 5V


| Celsius | HEX  | Decimal |
|---------|------|---------|
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |

## Temperature

| Celsius | HEX  | Decimal |
|---------|------|---------|
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |

## G-Force
DA4G-1  -  ACCELEROMETER G-FORCE MEASSURE:

0 - 4G range
1G = GRAVITY.   1 VOLT + 1 VOLT PR. G-FORCE. 2 Volt = 1G

## Temperature
DEGT-1   -  ”EGT” EXHAUST GAS TEMPERATURE MONITOR OPTION:
MEASSURE ON ANALOG 5-8 ON EXPANSION “1”
1 THERMOCOUPLE AMP BOX + CABLES + 2x ”K” THERMOCOUPLES

1 volt = 400
2 volt = 800
...

## Fuel pressure
Sensor DPS-270 (0-270 PSI) For fuel pressure:
0 PSI = 0,5V
30 PSI = 1V
60 PSI = 1,5V
90 PSI = 2V
270 PSI = 5V

# Bike setup:

## RPM sensors

TACH = Crankshaft magnet senor ( 2 magnets per rotation)

R_WHEEL = Output shaft backside of gear box

S4 = front of clutch (equal TACH x constant)

S3 = Unused

## Analog

Analog 1 = Fuel pressure

Analog 2 = G-force

Analog 3 = Oil pressure

Analog 4 = Gas handle

Analog 5 = Temperature front

Analog 6 = Temperature back

Analog 7 = Not in use

Analog 8 = Not in use

## Switches

Switch 1 = ?

Switch 2 = ?

Switch 3 = ?

Switch 4 = ?

## Legacy file format

OFFSET = 1178 bytes
CHUNK_SIZE = 38 bytes

<SAMPLE_ID_16_BIT><R_WHEEL_RPM_16_BIT><TACH_RPM_16_BIT><DIGITAL_16BIT><UNKNOWN_16bit><UNKNOWN_16bit><CLUTCH_SLIP_16bit><FUEL_PRESSURE_16bit><G_FORCE_16BIT><UNKNOWN_16bit><UNKNOWN_16bit><TEMP1_16BIT><TEMP2_16BIT><UNKNOWN_16bit><UNKNOWN_16bit><UNKNOWN_16bit><UNKNOWN_16bit><UNKNOWN_16bit><UNKNOWN_16bit>

# How to use

Install python 3.xx

    pip install matplotlib
    pip install pyserial
    pip install pyqt6

python parse_legacy.py  RUNDATA/MOSTEN20.ABQ/RUNTUE1.ABQ


# Bike gearing

Front 17 tooths
Rear 41 tooths

Left side
Front 66
Rear 76

