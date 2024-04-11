import sys

import download as dynalog
import plot as dynaplot

from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread

# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

# class Worker(QObject):
#     update_progress = pyqtSignal(int)

#     def do_work(self):
#         #dynalog.download(self.line_edit_com_port.text(), self.line_edit_event.text(), self.progress_callback)
#         dynalog.download("COM4", "Mosten", self.progress_callback)

#         # total_tasks = 100
#         # for i in range(total_tasks):

#         #     time.sleep(0.1)

#     def progress_callback(self, state, percentage):
#         """v"""
#         print(state)
#         print(percentage)
#         self.update_progress.emit(state, percentage)


class Worker(QObject):
    update_progress = pyqtSignal(str, int)

    stop_signal = pyqtSignal()  # Signal to stop the worker

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def do_work(self):
        # while not self.stop_signal.is_set():
        self.main_window.current_file = dynalog.download(self.main_window.line_edit_com_port.text(), self.main_window.line_edit_event.text(), self.progress)

    def progress(self, state, pct):
        self.update_progress.emit(state, 100 * pct // 62235 )


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynatek Datalogger")

        layout = QVBoxLayout()
        # widgets = [
        #     QCheckBox,
        #     QComboBox,
        #     QDateEdit,
        #     QDateTimeEdit,
        #     QDial,
        #     QDoubleSpinBox,
        #     QFontComboBox,
        #     QLCDNumber,
        #     QLabel,
        #     QLineEdit,
        #     QProgressBar,
        #     QPushButton,
        #     QRadioButton,
        #     QSlider,
        #     QSpinBox,
        #     QTimeEdit,
        # ]

        self.current_file = "data/event_2024-04-07_14-12-52_switch_1_2_3_4.log"

        self.line_edit_event = QLineEdit()
        event_layout = QHBoxLayout()
        event_layout.addWidget(QLabel("Event"))
        event_layout.addWidget(self.line_edit_event)
        self.line_edit_event.setText("Mosten Spring Race")


        self.line_edit_com_port = QLineEdit()
        com_layout = QHBoxLayout()
        com_layout.addWidget(QLabel("COM port"))
        com_layout.addWidget(self.line_edit_com_port)
        self.line_edit_com_port.setText("COM4")


        self.btn_download = QPushButton()
        self.btn_download.setEnabled(True)
        self.btn_download.setText("Download")

        self.btn_download.clicked.connect(self.download_clicked)

        layout.addLayout(com_layout)
        layout.addLayout(event_layout)
        layout.addWidget(self.btn_download)

        self.progress_download = QProgressBar()
        self.progress_download.minimum = 0
        self.progress_download.maximum = 100

        layout.addWidget(self.progress_download)

        widget = QWidget()
        widget.setLayout(layout)

        self.lbl_download_state = QLabel()
        self.lbl_download_state.setText("")

        self.btn_plot = QPushButton()
        self.btn_plot.setEnabled(False)
        self.btn_plot.setText("Plot")
        self.btn_plot.clicked.connect(self.plot_clicked)

        layout.addWidget(self.btn_plot)
        layout.addWidget(self.lbl_download_state)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

        self.worker = Worker(self)
        self.worker.update_progress.connect(self.update_progress)

    def update_progress(self, state, percentage):
        print(percentage)
        self.progress_download.setValue(percentage)
        self.lbl_download_state.setText(state)
        if state == "Done" or percentage == 100:
            self.btn_download.setEnabled(True)
            self.btn_plot.setEnabled(True)
            self.lbl_download_state.setText("Done")
            self.worker.stop_signal.emit()

    def download_clicked(self):
        self.btn_download.setEnabled(False)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.do_work)
        self.worker.stop_signal.connect(self.worker_thread.quit)
        self.worker_thread.start()

    def plot_clicked(self):
        """v"""
        print("Plot")
        #print(self.current_file)
        #if self.current_file > 0:
        dynaplot.parse_file(self.current_file, 27, 0)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()