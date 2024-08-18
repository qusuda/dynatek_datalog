import sys

import download as dynalog
import plot as dynaplot
import plot_pyqtgraph as dynapyplot

from PyQt6.QtCore import Qt, QObject, pyqtSignal, QThread, QSize

#from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QProgressBar, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
)

from PyQt6.QtGui import QPixmap

# QLCDNumber,
# QRadioButton,
# QSlider,
# QSpinBox,
# QTimeEdit,
# QCheckBox,
# QComboBox,
# QDateEdit,
# QDateTimeEdit,
# QDial,
# QDoubleSpinBox,
# QFontComboBox,

class Worker(QObject):
    update_progress = pyqtSignal(str, int)
    stop_signal = pyqtSignal()  # Signal to stop the worker

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.is_running = True

    def do_work(self):
        try:
            self.main_window.current_file = dynalog.download(
                self.main_window.line_edit_com_port.text(), 
                self.main_window.line_edit_event.text(), 
                self.progress
            )
            self.main_window.line_edit_file.setText(self.main_window.current_file)
        except Exception as e:
            self.update_progress.emit(f"Error: {str(e)}", 0)
        finally:
            self.is_running = False

    def progress(self, state, pct):
        self.update_progress.emit(state, pct)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynatek Datalogger")

        self.setFixedSize(QSize(600, 350))

        layout = QVBoxLayout()

        self.current_file = "Mosten Spring Race_2024-04-26_16-49-27.log"

        self.line_edit_event = QLineEdit()
        event_layout = QHBoxLayout()
        event_layout.addWidget(QLabel("Event"))
        event_layout.addWidget(self.line_edit_event)
        self.line_edit_event.setText("Mosten Raceday")

        self.line_edit_com_port = QLineEdit()
        com_layout = QHBoxLayout()
        com_layout.addWidget(QLabel("COM port"))
        com_layout.addWidget(self.line_edit_com_port)
        self.line_edit_com_port.setText("COM4")

        self.btn_download = QPushButton()
        self.btn_download.setEnabled(True)
        self.btn_download.setText("Download")

        self.btn_download.clicked.connect(self.download_clicked)

        # Create a label to display the image
        self.image_label = QLabel(self)
        
        # Load the image using QPixmap
        pixmap = QPixmap("resources/logo.png")  # Replace with your image path
        self.image_label.setPixmap(pixmap)
        
        # Adjust the label size to the image size
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(pixmap.size())

        layout.addWidget(self.image_label)
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

        # Create a button to open a file and plot data
        self.file_button = QPushButton("Select File")
        self.file_button.clicked.connect(self.open_file_dialog)

        self.line_edit_file = QLineEdit()
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("File"))
        file_layout.addWidget(self.line_edit_file)
        file_layout.addWidget(self.file_button)
        self.line_edit_file.setText(self.current_file)

        layout.addLayout(file_layout)

        self.btn_plot = QPushButton()
        self.btn_plot.setEnabled(True)
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
        self.progress_download.setValue(percentage)
        self.lbl_download_state.setText(state)
        if state == "Done" or "Error" in state:
            self.btn_download.setEnabled(True)
            self.btn_plot.setEnabled(state == "Done")
            self.worker.stop_signal.emit()

    def download_clicked(self):
        self.btn_download.setEnabled(False)
        # Create a new worker and thread each time a download is initiated
        self.worker = Worker(self)
        self.worker_thread = QThread()

        # Move the worker to the new thread
        self.worker.moveToThread(self.worker_thread)

        # Connect signals and slots
        self.worker_thread.started.connect(self.worker.do_work)
        self.worker.update_progress.connect(self.update_progress)
        self.worker.stop_signal.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.cleanup_after_download)

        # Start the thread
        self.worker_thread.start()

    def cleanup_after_download(self):
        # Re-enable the button after the work is done
        #self.btn_download.setEnabled(True)
        self.worker_thread = None  # Reset the thread reference

    def open_file_dialog(self):
        # Open a file dialog to select a file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "Log Files (*.log);;All Files (*)")
        if file_name:
            self.line_edit_file.setText(file_name)

    def plot_clicked(self):
        """v"""
        print(f"Plotting : {self.current_file}")
        #print(self.current_file)
        #if self.current_file > 0:
        self.current_file = self.line_edit_file.text() 
        data_points = dynaplot.parse_file(self.current_file, 27, 0)
        # Create a new window (QMainWindow or QWidget)
        self.new_window = dynapyplot.PlotApp()  # You can also use QWidget()        
        # Show the new window
        self.new_window.show()
        self.new_window.plot(data_points, self.current_file)
        self.new_window.updateViews()



app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()