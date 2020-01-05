import sys
from PyQt5 import QtCore, QtWidgets
from serialDevice import getSerialDevices, SerialGSMConnection
import threading
import time


class GUIMainWindow:
    cmd_monitor_max_lines = 25

    def __init__(self):
        self.main_window = QtWidgets.QMainWindow()
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget.setEnabled(False)
        self.footer_widget = QtWidgets.QWidget(self.main_window)

        self.discover_serial_btn = QtWidgets.QPushButton(self.central_widget)
        self.chose_device_lbl = QtWidgets.QLabel(self.central_widget)
        self.chose_device_combo = QtWidgets.QComboBox(self.central_widget)
        self.selected_device_lbl = QtWidgets.QLabel(self.central_widget)
        self.connection_btn = QtWidgets.QPushButton(self.central_widget)

        self.command_lbl = QtWidgets.QLabel(self.bottom_widget)
        self.command_line = QtWidgets.QLineEdit(self.bottom_widget)
        self.send_command_btn = QtWidgets.QPushButton(self.bottom_widget)
        self.cmd_monitor = QtWidgets.QListWidget(self.bottom_widget)
        self.cmd_monitor_list = []

        self.status_lbl = QtWidgets.QLabel(self.footer_widget)

        self.devices = []
        self.selected_device = None
        self.serial_conn = None

    def setup_window(self):
        self.setup_main_window()
        self.setup_central_widget()
        self.setup_bottom_widget()
        self.setup_footer_widget()

        self.add_discover_serial_btn()
        self.add_chose_device_lbl()
        self.add_chose_device_combo()
        self.set_selected_device_lbl()
        self.add_connection_button()

        self.add_cmd_lbl()
        self.add_cmd_line()
        self.add_send_cmd_btn()
        self.add_cmd_monitor_list()

        self.add_status_lbl()

        # self.retranslate_window()
        # QtCore.QMetaObject.connectSlotsByName(self.main_window)
        self.discover_serial_btn.clicked.connect(self.set_serial_devices)
        self.chose_device_combo.currentIndexChanged.connect(self.update_selected_device_lbl)
        self.connection_btn.clicked.connect(self.change_connection)
        self.send_command_btn.clicked.connect(self.send_command)
        self.command_line.returnPressed.connect(self.send_command)

    def setup_main_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.setGeometry(0, 0, 500, 550)
        self.main_window.setWindowTitle("GSM AT")

    def setup_central_widget(self):
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setGeometry(0, 0, 500, 200)

    def setup_bottom_widget(self):
        self.bottom_widget.setObjectName("BottomWidget")
        self.bottom_widget.setGeometry(0, 200, 500, 300)

    def setup_footer_widget(self):
        self.footer_widget.setObjectName("FooterWidget")
        self.footer_widget.setGeometry(0, 500, 500, 50)

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
        self.selected_device = self.devices[index].device
        self.selected_device_lbl.setText("Selected device: {}".format(self.selected_device))

    def add_connection_button(self):
        self.connection_btn.setGeometry(QtCore.QRect(10, 110, 100, 50))
        self.connection_btn.setText("Connect")
        self.connection_btn.setObjectName("ConnectionBtn")
        self.connection_btn.setEnabled(False)

    def change_connection(self):
        if self.serial_conn:
            self.close_connection()
        else:
            self.open_connection()

    def close_connection(self):
        if self.serial_conn:
            self.serial_conn = None
            self.connection_btn.setText("Connect")
            self.status_lbl.setText("device disconnected")
            self.chose_device_combo.setEnabled(True)
            self.status_lbl.setText("connection closed")
            self.bottom_widget.setEnabled(False)

    def open_connection(self):
        if not self.serial_conn:
            self.serial_conn = SerialGSMConnection(self.selected_device)
            success, reason = self.serial_conn.establish_connection()
            if success:
                self.connection_btn.setText("Disconnect")
                self.chose_device_combo.setEnabled(False)
                self.status_lbl.setText("connection established with {}".format(self.selected_device))
                self.bottom_widget.setEnabled(True)
                thread1 = threading.Thread(target=self.update_cmd_monitor_list)
                thread1.start()
            else:
                self.serial_conn = None
                self.status_lbl.setText(reason)
                QtWidgets.QMessageBox.about(self.main_window, "Error", reason)

    def add_cmd_lbl(self):
        self.command_lbl.setGeometry(10, 10, 400, 20)
        self.command_lbl.setText("Type Your Command")

    def add_cmd_line(self):
        self.command_line.setGeometry(QtCore.QRect(10, 30, 160, 20))
        self.command_line.setObjectName("CommandLine")

    def add_send_cmd_btn(self):
        self.send_command_btn.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.send_command_btn.setText("Send")
        self.send_command_btn.setObjectName("SendCmdBtn")

    def send_command(self):
        cmd = self.command_line.text()
        if cmd:
            self.command_line.clear()
            self.serial_conn.send_text_data(cmd)

    def add_cmd_monitor_list(self):
        self.cmd_monitor.setGeometry(QtCore.QRect(200, 10, 280, 250))
        self.cmd_monitor.setObjectName("CmdMonitor")
        self.cmd_monitor.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.cmd_monitor.setAutoScroll(True)

    def add_status_lbl(self):
        self.status_lbl.setGeometry(10, 30, 400, 20)
        self.status_lbl.setText("application started")

    def set_serial_devices(self):
        self.discover_serial_btn.setEnabled(False)
        self.connection_btn.setEnabled(False)
        self.selected_device = None
        self.close_connection()
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
        self.connection_btn.setEnabled(True)

    def update_cmd_monitor_list(self):
        while threading.main_thread().isAlive():
            if self.serial_conn:
                received_lines = self.serial_conn.receive_data()
                if received_lines:
                    self.cmd_monitor.addItems(received_lines)
                    time.sleep(0.1)
                    self.cmd_monitor.scrollToBottom()
            else:
                break

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
