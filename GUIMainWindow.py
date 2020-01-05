import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from serialDevice import getSerialDevices
import threading


class GUIMainWindow:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget = QtWidgets.QWidget(self.main_window)
        self.discover_serial_btn = QtWidgets.QPushButton(self.central_widget)
        self.chose_device_lbl = QtWidgets.QLabel(self.central_widget)
        self.chose_device_combo = QtWidgets.QComboBox(self.central_widget)
        self.selected_device_lbl = QtWidgets.QLabel(self.central_widget)
        self.status_lbl = QtWidgets.QLabel(self.bottom_widget)
        self.devices = []

    def setup_window(self):
        self.setup_main_window()
        self.setup_central_widget()
        self.setup_bottom_widget()
        self.add_discover_serial_btn()
        self.add_chose_device_lbl()
        self.add_chose_device_combo()
        self.set_selected_device_lbl()
        self.add_status_lbl()

        # self.retranslate_window()
        # QtCore.QMetaObject.connectSlotsByName(self.main_window)
        self.discover_serial_btn.clicked.connect(self.set_serial_devices)
        self.chose_device_combo.currentIndexChanged.connect(self.update_selected_device_lbl)

    def setup_main_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.setGeometry(0, 0, 500, 500)
        self.main_window.setWindowTitle("GSM AT")

    def setup_central_widget(self):
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setGeometry(0, 0, 500, 200)

    def setup_bottom_widget(self):
        self.bottom_widget.setObjectName("BottomWidget")
        self.bottom_widget.setGeometry(0, 200, 500, 300)

    def add_discover_serial_btn(self):
        self.discover_serial_btn.setGeometry(QtCore.QRect(10, 10, 100, 50))
        self.discover_serial_btn.setText("Discover \r\nSERIAL devices")
        self.discover_serial_btn.setObjectName("DiscoverSerialBtn")

    def add_chose_device_lbl(self):
        self.chose_device_lbl.setText("Select SERIAL DEVICE")
        self.chose_device_lbl.setGeometry(130, 10, 200, 20)

    def add_chose_device_combo(self):
        self.chose_device_combo.addItems([dev.__str__() for dev in self.devices])
        self.chose_device_combo.setGeometry(130, 30, 350, 30)

    def set_selected_device_lbl(self):
        self.selected_device_lbl.setText("Selected device:")
        self.selected_device_lbl.setGeometry(10, 80, 200, 20)

    def update_selected_device_lbl(self, index):
        self.selected_device_lbl.setText("Selected device: {}".format(self.devices[index].device))

    def add_status_lbl(self):
        self.status_lbl.setGeometry(10, 280, 400, 20)
        self.status_lbl.setText("application started")

    def set_serial_devices(self):
        self.discover_serial_btn.setEnabled(False)
        self.status_lbl.setText("device discovery started")
        thread1 = threading.Thread(target=self.discover_devices_in_bg)
        thread1.start()

    def discover_devices_in_bg(self):
        self.chose_device_combo.clear()
        self.devices = getSerialDevices()
        self.devices.reverse()
        self.chose_device_combo.addItems([dev.__str__() for dev in self.devices])
        self.status_lbl.setText("device discovery finished")
        self.discover_serial_btn.setEnabled(True)

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("MainWindow", "GSM AT"))
        self.discover_serial_btn.setText(_translate("MainWindow", "Discover \r\nSERIAL devices"))

    def show_window(self):
        self.main_window.show()


def start_app():
    app = QtWidgets.QApplication(sys.argv)
    ui = GUIMainWindow()
    ui.setup_window()
    ui.show_window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
