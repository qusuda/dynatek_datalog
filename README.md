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
| 100  | 3.3 | 0x7512|         | 
| 200  | 6.6 | 0x3B13|         | 
| 300  | 10  |       |         | 
| 500  | 20  |       |         | 
|1000  | 33.3| 0xB6E |         | 
|2000  | 66.6| 0x5D9 |         | 
|4000  | 133 | 0x2ED |         | 
|5000  | 166 |       |         | 
|8000  | 267 | 0x174 |         | 
|10000 | 333 |       |         | 

## S4 RPM 
This channel is reversed (higher frequency/RPM -> higher hex value)

S4 is front of clutch  

| RPM  | Hz  | HEX    | Decimal |
|------|-----|--------|---------|
|2000  | 66.6| 0x7E4  |         |
|4000  | 133 | 0xF9E  |         |
|8000  | 267 | 0x1F71 |         |

## Battery voltage

| Voltage | HEX  | Decimal |
|---------|------|---------|
| 10      | 0xA5 | 165     |
| 12      | 0xC6 | 198     |
| 14      | 0xE7 | 231     |

## Temperature

| Celsius | HEX  | Decimal |
|---------|------|---------|
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |
| ??      | 0x?? | ??     |


# Bike setup:

## RPM sensors

TACH = Crankshaft magnet senor ( 2 magnets per rotation)

R_WHEEL = Output shaft backside of gear box

S4 = front of clutch (equal TACH x constant)

S3 = Unused

## Analog

Analog 1 = Fuel pressure

Analog 2 = G-force

Analog 3 = ??

Analog 4 = Gas spjeld

Analog 5 = Temperature front

Analog 6 = Temperature back

Analog 7 = ?

Analog 8 = ?

## Switches

Switch 1 = ?

Switch 2 = ?

Switch 3 = ?

Switch 4 = ?



