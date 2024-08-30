"""Module for live data from Dynatek datalogger"""

import sys
import serial
import time

from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread, QSize

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QRadioButton, QLabel, QProgressBar


from data_point import DataPoint

# COM port settings
DEFAULT_COM_PORT = 'COM3'  # Change this to your COM port
BAUD_RATE = 9600



sim_file = ""
#sim_file = "test/input_simulation.log"



def live(port, live_data_cb):
    """Function downloading data"""
    ser = None
    sync = None

    chunk_bytes = bytearray()

    if len(sim_file) > 0:
        with open(sim_file, 'rb') as infile:
            print(f"Reading binary data from {port} to {sim_file}...")
            while True:
                # Read binary data from COM port
                data = infile.read(1)
                if data:
                    if data[0] == 0xAA:
                        sync = True
                    if sync:
                        # Write binary data to file
                        chunk_bytes.extend(data)
                        if len(chunk_bytes) == 27:
                            data_point = DataPoint(chunk_bytes)
                            chunk_bytes.clear()
                            sync = False
                            if data_point:
                                #data_point.print_live()
                                if live_data_cb:
                                    live_data_cb(data_point)
                else:
                    break
                time.sleep(0.0001)
    else:
        try:
            # Open COM port
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            if ser.is_open:
                print(f"Serial port {port} opened successfully.")
            print ("COM port opened")
            while True:
                # Read binary data from COM port
                data = ser.read(1)
                if data:
                    if data[0] == 0xAA:
                        sync = True
                    if sync:
                        # Write binary data to file
                        chunk_bytes.extend(data)
                        if len(chunk_bytes) == 27:
                            data_point = DataPoint(chunk_bytes)
                            chunk_bytes.clear()
                            sync = False
                            if data_point:
                                #data_point.print_live()
                                if live_data_cb:
                                    live_data_cb(data_point)
                # else:
                #     break
        except serial.SerialException as e:
            print(f"Error: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()
                print(f"Serial port {port} closed.")


class LiveWorker(QObject):
    update_live = pyqtSignal(DataPoint)
    stop_signal = pyqtSignal()  # Signal to stop the worker

    def __init__(self, main_window, com_port):
        super().__init__()
        self.main_window = main_window
        self.com_port = com_port
        self.is_running = True

    def do_work(self):
        live(self.com_port, self.live)

        # try:
        #     self.main_window.current_file = dynalog.download(
        #         self.main_window.line_edit_com_port.text(), 
        #         self.main_window.line_edit_event.text(), 
        #         self.progress
        #     )
        #     self.main_window.line_edit_file.setText(self.main_window.current_file)
        # except Exception as e:
        #     self.update_progress.emit(f"Error: {str(e)}", 0)
        # finally:
        #     self.is_running = False

    def live(self, data_point):
        self.update_live.emit(data_point)

class LiveApp(QMainWindow):
    def __init__(self, com_port):
        super().__init__()

        self.com_port = com_port

        # Set the window title
        self.setWindowTitle('Dynatek Datalogger - Live')

        self.setFixedSize(QSize(1024, 640))

        # Create a QWidget for the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout instance
        self.layout = QVBoxLayout(self.central_widget)

        # Event label
        self.event_label = QLabel('Live data')
        self.layout.addWidget(self.event_label)

        self.live_layout = QHBoxLayout()

        self.tach_view = QVBoxLayout()
        self.tach_rpm_view = QProgressBar()
        self.tach_rpm_view.setMinimum(0)
        self.tach_rpm_view.setMaximum(5000)
        self.tach_rpm_view.setOrientation(Qt.Orientation.Vertical)
        self.tach_rpm_label = QLabel("Value")
        self.tach_view.addWidget(self.tach_rpm_label)
        self.tach_view.addWidget(self.tach_rpm_view)
        self.tach_view.addWidget(QLabel("TACH"))

        self.rwhl_view = QVBoxLayout()
        self.rwhl_rpm_view = QProgressBar()
        self.rwhl_rpm_view.setMinimum(0)
        self.rwhl_rpm_view.setMaximum(5000)
        self.rwhl_rpm_view.setOrientation(Qt.Orientation.Vertical)
        self.rwhl_rpm_label = QLabel("Value")
        self.rwhl_view.addWidget(self.rwhl_rpm_label)
        self.rwhl_view.addWidget(self.rwhl_rpm_view)
        self.rwhl_view.addWidget(QLabel("RWHL"))

        self.s3_view = QVBoxLayout()
        self.s3_rpm_view = QProgressBar()
        self.s3_rpm_view.setMinimum(0)
        self.s3_rpm_view.setMaximum(5000)
        self.s3_rpm_view.setOrientation(Qt.Orientation.Vertical)
        self.s3_rpm_label = QLabel("Value")
        self.s3_view.addWidget(self.s3_rpm_label)
        self.s3_view.addWidget(self.s3_rpm_view)
        self.s3_view.addWidget(QLabel("S3"))

        self.s4_view = QVBoxLayout()
        self.s4_rpm_view = QProgressBar()
        self.s4_rpm_view.setMinimum(0)
        self.s4_rpm_view.setMaximum(5000)
        self.s4_rpm_view.setOrientation(Qt.Orientation.Vertical)
        self.s4_rpm_label = QLabel("Value")
        self.s4_view.addWidget(self.s4_rpm_label)
        self.s4_view.addWidget(self.s4_rpm_view)
        self.s4_view.addWidget(QLabel("S4"))

        self.temp_f_view = QVBoxLayout()
        self.temp_front_view = QProgressBar()
        self.temp_front_view.setMinimum(0)
        self.temp_front_view.setMaximum(800)
        self.temp_front_view.setOrientation(Qt.Orientation.Vertical)
        self.temp_front_label = QLabel("Value")
        self.temp_f_view.addWidget(self.temp_front_label)
        self.temp_f_view.addWidget(self.temp_front_view)
        self.temp_f_view.addWidget(QLabel("Temp. Front"))

        self.temp_b_view = QVBoxLayout()
        self.temp_back_view = QProgressBar()
        self.temp_back_view.setMinimum(0)
        self.temp_back_view.setMaximum(800)
        self.temp_back_view.setOrientation(Qt.Orientation.Vertical)
        self.temp_back_label = QLabel("Value")
        self.temp_b_view.addWidget(self.temp_back_label)
        self.temp_b_view.addWidget(self.temp_back_view)
        self.temp_b_view.addWidget(QLabel("Temp. Back"))

        self.throttle_view = QVBoxLayout()
        self.throttle_percent_view = QProgressBar()
        self.throttle_percent_view.setMinimum(0)
        self.throttle_percent_view.setMaximum(100)
        self.throttle_percent_view.setOrientation(Qt.Orientation.Vertical)
        self.throttle_label = QLabel("Value")
        self.throttle_view.addWidget(self.throttle_label)
        self.throttle_view.addWidget(self.throttle_percent_view)
        self.throttle_view.addWidget(QLabel("Throttle"))

        self.fuel_p_view = QVBoxLayout()
        self.fuel_pressure_view = QProgressBar()
        self.fuel_pressure_view.setMinimum(0)
        self.fuel_pressure_view.setMaximum(800)
        self.fuel_pressure_view.setOrientation(Qt.Orientation.Vertical)
        self.fuel_pressure_label = QLabel("Value")
        self.fuel_p_view.addWidget(self.fuel_pressure_label)
        self.fuel_p_view.addWidget(self.fuel_pressure_view)
        self.fuel_p_view.addWidget(QLabel("Fuel pressure"))

        self.g_force_view = QVBoxLayout()
        self.g_force_g_view = QProgressBar()
        self.g_force_g_view.setMinimum(0)
        self.g_force_g_view.setMaximum(40)
        self.g_force_g_view.setOrientation(Qt.Orientation.Vertical)
        self.g_force_label = QLabel()
        self.g_force_view.addWidget(self.g_force_label)
        self.g_force_view.addWidget(self.g_force_g_view)
        self.g_force_view.addWidget(QLabel("G-force"))

        self.battery_view = QVBoxLayout()
        self.battery_voltage_view = QProgressBar()
        self.battery_voltage_view.setMinimum(0)
        self.battery_voltage_view.setMaximum(150)
        self.battery_voltage_view.setOrientation(Qt.Orientation.Vertical)
        self.batt_voltage_label = QLabel()
        self.battery_view.addWidget(self.batt_voltage_label)
        self.battery_view.addWidget(self.battery_voltage_view)
        self.battery_view.addWidget(QLabel("Battery Voltage"))

        self.live_layout.addLayout(self.tach_view)
        self.live_layout.addLayout(self.rwhl_view)
        self.live_layout.addLayout(self.s3_view)
        self.live_layout.addLayout(self.s4_view)
        self.live_layout.addLayout(self.temp_f_view)
        self.live_layout.addLayout(self.temp_b_view)
        self.live_layout.addLayout(self.throttle_view)
        self.live_layout.addLayout(self.fuel_p_view)
        self.live_layout.addLayout(self.g_force_view)
        self.live_layout.addLayout(self.battery_view)

        self.layout.addLayout(self.live_layout)

        self.sw1_button = QCheckBox("Switch 1 (Gear)")
        self.sw2_button = QCheckBox("Switch 2")
        self.sw3_button = QCheckBox("Switch 3")
        self.sw4_button = QCheckBox("Switch 4")

        self.sw_layout = QHBoxLayout()
        self.sw_layout.addWidget(self.sw1_button)
        self.sw_layout.addWidget(self.sw2_button)
        self.sw_layout.addWidget(self.sw3_button)
        self.sw_layout.addWidget(self.sw4_button)
        self.layout.addLayout(self.sw_layout)

    def live_data_callback(self, data_point):
        print(f"Callback function called with result: {data_point}")

    def start(self):
        # Create a new worker and thread each time a Live session
        self.live_worker = LiveWorker(self, self.com_port)
        self.live_worker_thread = QThread()

        # Move the worker to the new thread
        self.live_worker.moveToThread(self.live_worker_thread)

        # Connect signals and slots
        self.live_worker_thread.started.connect(self.live_worker.do_work)
        self.live_worker.update_live.connect(self.update_live)
        self.live_worker.stop_signal.connect(self.live_worker_thread.quit)
        #self.live_worker_thread.finished.connect(self.live_worker_thread.deleteLater)
        #self.live_worker_thread.finished.connect(self.live_worker_thread.cleanup_after_download)

        # Start the thread
        self.live_worker_thread.start()

    def update_live(self, data_point):
        data_point.print_live()
        self.tach_rpm_view.setValue(data_point.tach_rpm)
        self.tach_rpm_label.setText(str(data_point.tach_rpm) + " RPM")

        self.rwhl_rpm_view.setValue(data_point.rwhl_rpm)
        self.rwhl_rpm_label.setText(str(data_point.rwhl_rpm) + " RPM")
        self.s3_rpm_view.setValue(data_point.s3_rpm)
        self.s3_rpm_label.setText(str(data_point.s3_rpm) + " RPM")
        self.s4_rpm_view.setValue(data_point.s4_rpm)
        self.s4_rpm_label.setText(str(data_point.s4_rpm) + " RPM")

        self.temp_front_view.setValue(int(data_point.temperature_front))
        self.temp_front_label.setText("{:.1f} C".format(data_point.temperature_front))
        self.temp_back_view.setValue(int(data_point.temperature_back))
        self.temp_back_label.setText("{:.1f} C".format(data_point.temperature_back))

        self.throttle_percent_view.setValue(int(data_point.throttle))
        self.throttle_label.setText("{:.0f} %".format(data_point.throttle))
        self.fuel_pressure_view.setValue(int(data_point.fuel_pressure))
        self.fuel_pressure_label.setText("{:.1f} PSI".format(data_point.fuel_pressure))

        self.g_force_g_view.setValue(int(data_point.g_force*10))
        self.g_force_label.setText("{:.2f} G".format(data_point.g_force))
        
        self.battery_voltage_view.setValue(int(data_point.battery_voltage*10))
        self.batt_voltage_label.setText("{:.1f} volt".format(data_point.battery_voltage))

        self.sw1_button.setChecked(data_point.switch1)
        self.sw2_button.setChecked(data_point.switch2)
        self.sw3_button.setChecked(data_point.switch3)
        self.sw4_button.setChecked(data_point.switch4)

def live_cb(data_point):
    data_point.print_live()



if __name__ == "__main__":
    COM_PORT = DEFAULT_COM_PORT
    EVENT_NAME = "event"

    if len(sys.argv) < 2:
        print("Usage: python live.py <COM_port>")

    if len(sys.argv) > 1:
        COM_PORT = sys.argv[1]

    live(COM_PORT, live_cb)
