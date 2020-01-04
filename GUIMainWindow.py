import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from serialDevice import getSerialDevices
import threading


class GUIMainWindow:
    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = None
        self.devices = []
        # self.lock = threading.Lock()

    def setup_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.setGeometry(0, 0, 500, 500)
        self.main_window.setWindowTitle("GSM AT")

        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setGeometry(0, 0, 500, 200)

        self.bottom_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget.setObjectName("BottomWidget")
        self.bottom_widget.setGeometry(0, 200, 500, 300)

        self.add_discover_serial_btn()

        self.chose_device_lbl = QtWidgets.QLabel(self.central_widget)
        self.chose_device_lbl.setText("SERIAL DEVICES")
        self.chose_device_lbl.setGeometry(130, 10, 100, 20)

        self.chose_device_combo = QtWidgets.QComboBox(self.central_widget)
        self.chose_device_combo.addItems([dev.__str__() for dev in self.devices])
        self.chose_device_combo.setGeometry(130, 30, 350, 30)

        self.statusLbl = QtWidgets.QLabel(self.bottom_widget)
        self.statusLbl.setGeometry(10, 280, 400, 20)
        self.statusLbl.setText("application started")

        self.retranslate_window()

        # QtCore.QMetaObject.connectSlotsByName(self.main_window)
        self.discover_serial_btn.clicked.connect(self.setSerialDevices)

    def add_discover_serial_btn(self):
        self.discover_serial_btn = QtWidgets.QPushButton(self.central_widget)
        self.discover_serial_btn.setGeometry(QtCore.QRect(10, 10, 100, 50))
        # self.selectImageBtn.setFont(self.font)
        self.discover_serial_btn.setObjectName("DiscoverSerialBtn")

    def setSerialDevices(self):
        self.discover_serial_btn.setEnabled(False)
        self.statusLbl.setText("device discovery started")
        thread1 = threading.Thread(target=self.discover_devices_in_bg)
        thread1.start()

    def discover_devices_in_bg(self):
        self.chose_device_combo.clear()
        self.devices = getSerialDevices()
        self.chose_device_combo.addItems([dev.__str__() for dev in self.devices])
        self.statusLbl.setText("device discovery finished")
        self.discover_serial_btn.setEnabled(True)

    def retranslate_window(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("MainWindow", "GSM AT"))
        self.discover_serial_btn.setText(_translate("MainWindow", "Discover \r\nSERIAL devices"))

        # self.Combo.setText(_translate("MainWindow", "Select Image"))

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
