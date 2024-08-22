import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QLabel
import pyqtgraph as pg

import parse as dynaplot

class PlotApp(QMainWindow):
    # Set global axix width to align plot i stack
    axis_width = 50
    # State variable for "show" checkboxes
    show_force = True
    show_throttle = True
    show_gear_switch = True
    show_temperature = True

    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Dynatek Datalogger - Plot')

        # Create a QWidget for the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout instance
        self.layout = QVBoxLayout(self.central_widget)

        # Event label
        self.event_label = QLabel('Event')
        self.layout.addWidget(self.event_label)

        # Create a QHBoxLayout instance
        hbox_layout = QHBoxLayout()

        # Create QCheckBox instance instances "Show"
        self.g_force_checkbox = QCheckBox('G-Force', self)
        self.temperature_checkbox = QCheckBox('Temperature', self)
        self.gear_switch_checkbox = QCheckBox('Gear', self)
        self.throttle_checkbox = QCheckBox('Throttle/Fuel Pressure', self)
        
        # Set Intial checkbox states
        self.g_force_checkbox.setChecked(self.show_force)
        self.temperature_checkbox.setChecked(self.show_temperature)
        self.gear_switch_checkbox.setChecked(self.show_gear_switch)
        self.throttle_checkbox.setChecked(self.show_throttle)

        # Connect state handlers
        self.g_force_checkbox.stateChanged.connect(self.onGForceCheckBoxStateChanged)
        self.temperature_checkbox.stateChanged.connect(self.onTemperatureCheckBoxStateChanged)
        self.gear_switch_checkbox.stateChanged.connect(self.onGearSwitchCheckBoxStateChanged)
        self.throttle_checkbox.stateChanged.connect(self.onThrottleCheckBoxStateChanged)

        # Add the QCheckBox'es to the horizontal layout
        hbox_layout.addWidget(self.g_force_checkbox)
        hbox_layout.addWidget(self.temperature_checkbox)
        hbox_layout.addWidget(self.gear_switch_checkbox)
        hbox_layout.addWidget(self.throttle_checkbox)

        # Add horizontal box layput to main layout
        self.layout.addLayout(hbox_layout)
        
        # Battery voltage label
        self.battery_voltage_label = QLabel('Battery voltage : 14.0 volt')
        self.layout.addWidget(self.battery_voltage_label)

        # Create a pyqtgraph PlotWidget instance
        self.rpm_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.rpm_plot_widget)

        # Enabled X mouse handling on RPM plot
        self.rpm_plot_widget.setMouseEnabled(x=True,y=False)

        self.rpm_plot_widget.plotItem.addLegend()

        # Add cursor
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.rpm_plot_widget.addItem(self.vLine, ignoreBounds=True)

        # Cursor position label
        self.cursor_label = QLabel('')
        self.layout.addWidget(self.cursor_label)

        # Connect mouse move event to RPM Plot
        self.rpm_plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)

        # Create a Temp PlotWidget instance
        self.temp_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.temp_plot_widget)
        # Enabled X-ais mouse event on temperature plot
        self.temp_plot_widget.setMouseEnabled(x=True,y=False)

        # Add cursor to throttle plot
        self.temp_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.temp_plot_widget.addItem(self.temp_vLine, ignoreBounds=True)
        self.temp_plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)
        self.temp_plot_widget.plotItem.addLegend()

        # Create a Throttle PlotWidget instance
        self.throttle_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.throttle_plot_widget)
        # Enabled X-ais mouse event on throttle plot
        self.throttle_plot_widget.setMouseEnabled(x=True,y=False)
        # Add cursor to throttle plot
        self.throttle_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.throttle_plot_widget.addItem(self.throttle_vLine, ignoreBounds=True)
        self.throttle_plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)

        # Create a g-force PlotWidget instance
        self.g_force_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.g_force_plot_widget)
        # Enable X-ais mouse event on g force plot
        self.g_force_plot_widget.setMouseEnabled(x=True,y=False)
        # Add cursor to g force
        self.g_force_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.g_force_plot_widget.addItem(self.g_force_vLine, ignoreBounds=True)
        self.g_force_plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)


        # Create a gear PlotWidget instance
        self.gear_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.gear_plot_widget)
        # Enable X-ais mouse event on gear plot plot
        self.gear_plot_widget.setMouseEnabled(x=True,y=False)
        # Add cursor to throttle plot
        self.gear_vLine = pg.InfiniteLine(angle=90, movable=False)
        self.gear_plot_widget.addItem(self.gear_vLine, ignoreBounds=True)
        self.gear_plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)

        # Set fixed height on gear plot
        self.gear_plot_widget.setFixedHeight(70)


        # # Initialize ROI
        # self.roi = pg.ROI([1, 10], [1, 100])
        # self.rpm_plot_widget.addItem(self.roi)

        # # Connect the ROI to a callback
        # self.roi.sigRegionChanged.connect(self.update_roi)

        # Set axis labels with units
        self.rpm_plot_widget.plotItem.setLabel('left', 'RPM')
        # Create the secondary y-axis view box
        self.p2 = pg.ViewBox()
        self.rpm_plot_widget.plotItem.showAxis('right')
        self.rpm_plot_widget.plotItem.setLabel('right', 'Clutch slip')
        self.rpm_plot_widget.plotItem.scene().addItem(self.p2)
        self.rpm_plot_widget.plotItem.getAxis('right').linkToView(self.p2)
        self.p2.setXLink(self.rpm_plot_widget.plotItem)

        # Attach the update function to both views
        self.rpm_plot_widget.plotItem.vb.sigResized.connect(self.updateViews)
        
        # Plot data on the secondary y-axis (( CLUTCH SLIP))
        secondary_curve = pg.PlotDataItem([0, 1, 2, 3, 4, 5, 20], [100, 80, 77, 70, 20, 10, 0], pen='orange')
        self.p2.addItem(secondary_curve)

        #self.rpm_plot_widget.plotItem.setLabel('bottom', 'Time', units='s')


        self.temp_plot_widget.plotItem.setLabel('left', 'Temperature', units='°C')
        #self.temp_plot_widget.plotItem.setLabel('bottom', 'Time', units='s')

        self.throttle_plot_widget.plotItem.setLabel('left', 'Throttle', units='%')
        self.throttle_plot_widget.plotItem.addLegend()
        #self.throttle_plot_widget.plotItem.setLabel('bottom', 'Time', units='s')

        self.g_force_plot_widget.plotItem.setLabel('left', 'G-Force', units='g')
        #self.g_force_plot_widget.plotItem.setLabel('bottom', 'Time', units='s')

        self.gear_plot_widget.plotItem.setLabel('left', 'Gear', units='')
        self.gear_plot_widget.plotItem.setLabel('bottom', 'Time', units='s')

        # Track which plot is sending the signal to prevent infinite loop
        self.senderPlot = None

        # Link the x-axes (zoom and position)
        self.rpm_plot_widget.getViewBox().sigXRangeChanged.connect(self.syncX)
        self.temp_plot_widget.getViewBox().sigXRangeChanged.connect(self.syncX)
        self.throttle_plot_widget.getViewBox().sigXRangeChanged.connect(self.syncX)
        self.gear_plot_widget.getViewBox().sigXRangeChanged.connect(self.syncX)
        self.g_force_plot_widget.getViewBox().sigXRangeChanged.connect(self.syncX)


    def onGForceCheckBoxStateChanged(self, state):
        if state == 2:  # Checked
            self.show_force = True
            self.layout.addWidget(self.g_force_plot_widget)
        else:  # Unchecked
            self.layout.removeWidget(self.g_force_plot_widget)
            self.g_force_plot_widget.setParent(None)
            self.show_force = False

    def onTemperatureCheckBoxStateChanged(self, state):
        if state == 2:  # Checked
            self.show_temperature = True
            self.layout.addWidget(self.temp_plot_widget)
        else:  # Unchecked
            self.layout.removeWidget(self.temp_plot_widget)
            self.temp_plot_widget.setParent(None)
            self.show_temperature = False

    def onGearSwitchCheckBoxStateChanged(self, state):
        if state == 2:  # Checked
            self.show_gear_switch = True
            self.layout.addWidget(self.gear_plot_widget)
        else:  # Unchecked
            self.layout.removeWidget(self.gear_plot_widget)
            self.gear_plot_widget.setParent(None)
            self.show_gear_switch = False

    def onThrottleCheckBoxStateChanged(self, state):
        if state == 2:  # Checked
            self.show_throttle = True
            self.layout.addWidget(self.throttle_plot_widget)
        else:  # Unchecked
            self.layout.removeWidget(self.throttle_plot_widget)
            self.throttle_plot_widget.setParent(None)
            self.show_throttle = False

    # Define update function to sync views
    def updateViews(self):
        self.p2.setGeometry(self.rpm_plot_widget.plotItem.vb.sceneBoundingRect())
        self.p2.linkedViewChanged(self.rpm_plot_widget.plotItem.vb, self.p2.XAxis)

    # Link cursors
    def mouseMoved(self, event):
        pos = event  # Using the event directly
        current_widget = None
        if self.rpm_plot_widget.sceneBoundingRect().contains(pos):
            current_widget = self.rpm_plot_widget
        if self.temp_plot_widget.sceneBoundingRect().contains(pos):
            current_widget = self.temp_plot_widget
        if self.throttle_plot_widget.sceneBoundingRect().contains(pos):
            current_widget = self.throttle_plot_widget
        if self.g_force_plot_widget.sceneBoundingRect().contains(pos):
            current_widget = self.g_force_plot_widget
        if self.gear_plot_widget.sceneBoundingRect().contains(pos):
            current_widget = self.gear_plot_widget
        
        mousePoint = current_widget.plotItem.vb.mapSceneToView(pos)
        self.vLine.setPos(mousePoint.x())
        self.temp_vLine.setPos(mousePoint.x())
        self.throttle_vLine.setPos(mousePoint.x())
        self.g_force_vLine.setPos(mousePoint.x())
        self.gear_vLine.setPos(mousePoint.x())
        self.cursor_label.setText(f'Time: {mousePoint.x():.2f}, RPM: {mousePoint.y():.0f}')

    def plot(self, data_points, event):
        print("Plot")

        self.event_label.setText(f'<H1>{event}</H1>')

        # Extracting data members for plotting
        sample_ids = [float(data_point.sample_id) / 100 for data_point in data_points]

        #battery_voltage = [data_point.battery_voltage for data_point in data_points]

        tach_rpms = [data_point.tach_rpm for data_point in data_points]
        rwhl_rpms = [data_point.rwhl_rpm for data_point in data_points]
        #clutch_slip = [data_point.clutch_slip for data_point in data_points]
        s3_rpms = [data_point.s3_rpm for data_point in data_points]

        s4_rpms = [data_point.s4_rpm for data_point in data_points]

        fuel_pressure = [data_point.fuel_pressure for data_point in data_points]
        g_force = [data_point.g_force for data_point in data_points]
        throttle = [data_point.throttle for data_point in data_points]
        
        temp_front = [data_point.temperature_front for data_point in data_points]
        temp_back = [data_point.temperature_back for data_point in data_points]

        switch1 = [data_point.switch1 for data_point in data_points]

        # Plot data on respective plot widgets
        self.rpm_plot_widget.plot(sample_ids, tach_rpms, pen='b', name='Tach')
        self.rpm_plot_widget.plot(sample_ids, s3_rpms, pen='g', name='R_whl')
        self.rpm_plot_widget.plotItem.getAxis('left').setWidth(int(self.axis_width))
        self.rpm_plot_widget.plotItem.getAxis('right').setWidth(int(40))
        
        self.temp_plot_widget.plot(sample_ids, temp_front, pen='r', name='Front')
        self.temp_plot_widget.plot(sample_ids, temp_back, pen='y', name='Back')
        self.temp_plot_widget.plotItem.getAxis('left').setWidth(int(self.axis_width))
        self.temp_plot_widget.plotItem.showAxis('right')
        self.temp_plot_widget.plotItem.getAxis('right').setWidth(int(40))
        
        self.throttle_plot_widget.plot(sample_ids, throttle, pen='pink', name = 'Throttle')
        self.throttle_plot_widget.plot(sample_ids, fuel_pressure, pen='cyan', name = 'Pressure')
        self.throttle_plot_widget.plotItem.getAxis('left').setWidth(int(self.axis_width))
        self.throttle_plot_widget.plotItem.showAxis('right')
        self.throttle_plot_widget.plotItem.getAxis('right').setWidth(int(40))

        self.g_force_plot_widget.plot(sample_ids, g_force, pen='green')
        self.g_force_plot_widget.plotItem.getAxis('left').setWidth(int(self.axis_width))
        self.g_force_plot_widget.plotItem.showAxis('right')
        self.g_force_plot_widget.plotItem.getAxis('right').setWidth(int(40))

        self.gear_plot_widget.plot(sample_ids, switch1, pen='b')
        self.gear_plot_widget.plotItem.getAxis('left').setWidth(int(self.axis_width))
        self.gear_plot_widget.plotItem.showAxis('right')
        self.gear_plot_widget.plotItem.getAxis('right').setWidth(int(40))

    def update_roi(self):
        roi_bounds = self.roi.getArraySlice(self.rpm_plot_widget.imageItem.image, self.rpm_plot_widget.imageItem)
        print("ROI bounds:", roi_bounds)


    def syncX(self, viewBox):
        if self.senderPlot is not None:
            return

        # Determine which plot sent the signal
        self.senderPlot = viewBox

        # Get the view range of the sender plot
        xRange, _ = viewBox.viewRange()

        # Apply the view range to other plots
        if self.senderPlot != self.rpm_plot_widget.getViewBox():
            self.rpm_plot_widget.getViewBox().setXRange(*xRange, padding=0)
        if self.senderPlot != self.temp_plot_widget.getViewBox():
            self.temp_plot_widget.getViewBox().setXRange(*xRange, padding=0)
        if self.senderPlot != self.throttle_plot_widget.getViewBox():
            self.throttle_plot_widget.getViewBox().setXRange(*xRange, padding=0)
        if self.senderPlot != self.gear_plot_widget.getViewBox():
            self.gear_plot_widget.getViewBox().setXRange(*xRange, padding=0)
        if self.senderPlot != self.g_force_plot_widget.getViewBox():
            self.g_force_plot_widget.getViewBox().setXRange(*xRange, padding=0)

        self.senderPlot = None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    current_file = 'Mosten Spring Race_2024-04-26_16-49-27.log'
    print(f"Plotting : {current_file}")
    data_points = dynaplot.parse_file(current_file, 27, 0)

    # Create the main window
    main_window = PlotApp()
    main_window.show()
    main_window.plot(data_points, current_file)
    main_window.updateViews()

    # Execute the application
    sys.exit(app.exec())