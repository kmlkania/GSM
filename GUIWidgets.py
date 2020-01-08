from PyQt5 import QtCore, QtWidgets
from GUIElements import GUIElements
import threading
import time
from DeviceManager import DeviceManager


class GUIWidget:
    def __init__(self, main_widow):
        self.main_window = main_widow
        self.head_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget = QtWidgets.QWidget(self.main_window)
        self.bottom_widget.setEnabled(False)
        self.footer_widget = QtWidgets.QWidget(self.main_window)
        self.head_widget_elements = {}
        self.bottom_widget_elements = {}
        self.footer_widget_elements = {}
        self.device_manager = DeviceManager(self)
        self.cmd_monitor_list = []

    def setup_head_widget(self):
        self.head_widget.setObjectName("CentralWidget")
        self.head_widget.setGeometry(QtCore.QRect(0, 0, 500, 200))
        self.setup_head_widget_content()
        return self.head_widget

    def setup_bottom_widget(self):
        self.bottom_widget.setObjectName("BottomWidget")
        self.bottom_widget.setGeometry(0, 200, 500, 300)
        self.setup_bottom_widget_content()
        return self.bottom_widget

    def setup_footer_widget(self):
        self.footer_widget.setObjectName("FooterWidget")
        self.footer_widget.setGeometry(0, 500, 500, 50)
        self.setup_footer_widget_content()
        return self.footer_widget

    def setup_head_widget_content(self):
        self.head_widget_elements['discover_serial_btn'] = GUIElements.add_push_btn(
            self.head_widget, QtCore.QRect(10, 10, 100, 50), "DiscoverSerialBtn", "Discover \r\nSERIAL devices")
        self.head_widget_elements['chose_device_lbl'] = \
            GUIElements.add_lbl(self.head_widget, QtCore.QRect(130, 10, 200, 20), "Select SERIAL DEVICE")
        self.head_widget_elements['chose_device_combo'] = \
            GUIElements.add_combo_box(self.head_widget, QtCore.QRect(130, 30, 350, 30))
        self.head_widget_elements['selected_device_lbl'] = \
            GUIElements.add_lbl(self.head_widget, QtCore.QRect(10, 80, 200, 20), "Selected device:")
        self.head_widget_elements['connection_btn'] = \
            GUIElements.add_push_btn(self.head_widget, QtCore.QRect(10, 110, 100, 50), "ConnectionBtn", "Connect")
        self.head_widget_elements['connection_btn'].setEnabled(False)

    def setup_bottom_widget_content(self):
        self.bottom_widget_elements['command_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 10, 400, 20), "Type Your Command")
        self.bottom_widget_elements['command_line'] = \
            GUIElements.add_line_edit(self.bottom_widget, QtCore.QRect(10, 30, 160, 20), "CommandLine")
        self.bottom_widget_elements['send_command_btn'] = \
            GUIElements.add_push_btn(self.bottom_widget, QtCore.QRect(10, 50, 100, 30), "SendCmdBtn", "Send")
        self.bottom_widget_elements['cmd_monitor'] = GUIElements.add_list_w(
            self.bottom_widget, QtCore.QRect(200, 10, 280, 250), QtWidgets.QAbstractItemView.NoSelection, "CmdMonitor")
        self.bottom_widget_elements['cmd_monitor'].setAutoScroll(True)

    def setup_footer_widget_content(self):
        self.footer_widget_elements['status_lbl'] = \
            GUIElements.add_lbl(self.footer_widget, QtCore.QRect(10, 30, 400, 20), "application started")

    def setup_actions(self):
        self.head_widget_elements['discover_serial_btn'].clicked.connect(self.device_manager.set_serial_devices)
        self.head_widget_elements['chose_device_combo'].currentIndexChanged.connect(
            self.device_manager.update_selected_device_lbl)
        self.head_widget_elements['connection_btn'].clicked.connect(self.device_manager.change_connection)
        self.bottom_widget_elements['send_command_btn'].clicked.connect(self.send_command)
        self.bottom_widget_elements['command_line'].returnPressed.connect(self.send_command)

    def send_command(self):
        cmd = self.bottom_widget_elements['command_line'].text()
        if cmd:
            self.bottom_widget_elements['command_line'].clear()
            self.device_manager.send_command(cmd)

    def update_cmd_monitor_list(self):
        while threading.main_thread().isAlive():
            if self.device_manager.has_active_connection:
                received_lines = self.device_manager.get_data_from_device()
                if received_lines:
                    self.bottom_widget_elements['cmd_monitor'].addItems(received_lines)
                    self.bottom_widget_elements['cmd_monitor'].addItem('')
                    time.sleep(0.1)
                    self.bottom_widget_elements['cmd_monitor'].scrollToBottom()
            else:
                break

    def pop_up_alert(self, title, message):
        self.footer_widget_elements['status_lbl'].setText(message)
        QtWidgets.QMessageBox.about(self.main_window, title, message)
