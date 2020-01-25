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
        self.head_widget.setGeometry(QtCore.QRect(0, 0, 550, 120))
        self.setup_head_widget_content()
        return self.head_widget

    def setup_bottom_widget(self):
        self.bottom_widget.setObjectName("BottomWidget")
        self.bottom_widget.setGeometry(0, 120, 550, 380)
        self.setup_bottom_widget_content()
        return self.bottom_widget

    def setup_footer_widget(self):
        self.footer_widget.setObjectName("FooterWidget")
        self.footer_widget.setGeometry(0, 500, 550, 50)
        self.setup_footer_widget_content()
        return self.footer_widget

    def setup_head_widget_content(self):
        self.head_widget_elements['discover_serial_btn'] = GUIElements.add_push_btn(
            self.head_widget, QtCore.QRect(10, 10, 90, 50), "DiscoverSerialBtn", "Discover \r\nSERIAL devices")
        self.head_widget_elements['chose_device_lbl'] = \
            GUIElements.add_lbl(self.head_widget, QtCore.QRect(110, 10, 200, 20), "Select SERIAL DEVICE")
        self.head_widget_elements['chose_device_combo'] = \
            GUIElements.add_combo_box(self.head_widget, QtCore.QRect(110, 30, 350, 30))
        self.head_widget_elements['selected_device_lbl'] = \
            GUIElements.add_lbl(self.head_widget, QtCore.QRect(10, 80, 200, 20), "Selected device:")
        self.head_widget_elements['connection_btn'] = \
            GUIElements.add_push_btn(self.head_widget, QtCore.QRect(470, 10, 70, 50), "ConnectionBtn", "Connect")
        self.head_widget_elements['connection_btn'].setEnabled(False)

    def setup_bottom_widget_content(self):
        self.setup_command_interface()
        self.bottom_widget_elements['cmd_monitor'] = GUIElements.add_list_w(
            self.bottom_widget, QtCore.QRect(200, 10, 340, 370), QtWidgets.QAbstractItemView.NoSelection, "CmdMonitor")
        self.bottom_widget_elements['cmd_monitor'].setAutoScroll(True)
        self.setup_ussd_interface()
        self.setup_sms_interface()

    def setup_footer_widget_content(self):
        self.footer_widget_elements['status_lbl'] = \
            GUIElements.add_lbl(self.footer_widget, QtCore.QRect(10, 30, 400, 20), "application started")

    def setup_actions(self):
        self.head_widget_elements['discover_serial_btn'].clicked.connect(self.device_manager.set_serial_devices)
        self.head_widget_elements['chose_device_combo'].currentIndexChanged.connect(
            self.device_manager.update_selected_device)
        self.head_widget_elements['connection_btn'].clicked.connect(self.device_manager.change_connection)
        self.bottom_widget_elements['send_command_btn'].clicked.connect(self.send_command)
        self.bottom_widget_elements['command_line'].returnPressed.connect(self.send_command)
        self.bottom_widget_elements['ussd_line'].returnPressed.connect(self.send_ussd)
        self.bottom_widget_elements['send_ussd_btn'].clicked.connect(self.send_ussd)
        self.bottom_widget_elements['send_sms_btn'].clicked.connect(self.send_sms)

    def setup_command_interface(self):
        self.bottom_widget_elements['command_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 10, 400, 20), "Type Your Command")
        self.bottom_widget_elements['command_line'] = \
            GUIElements.add_line_edit(self.bottom_widget, QtCore.QRect(10, 30, 160, 20), "CommandLine")
        self.bottom_widget_elements['send_command_btn'] = \
            GUIElements.add_push_btn(self.bottom_widget, QtCore.QRect(10, 50, 100, 20), "SendCmdBtn", "Send")

    def setup_ussd_interface(self):
        self.bottom_widget_elements['ussd_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 80, 400, 20), "Type Your USSD")
        self.bottom_widget_elements['ussd_line'] = \
            GUIElements.add_line_edit(self.bottom_widget, QtCore.QRect(10, 100, 160, 20), "USSDLine")
        self.bottom_widget_elements['send_ussd_btn'] = \
            GUIElements.add_push_btn(self.bottom_widget, QtCore.QRect(10, 120, 100, 20), "SendUSSDBtn", "Send")

    def setup_sms_interface(self):
        self.bottom_widget_elements['sms_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 150, 400, 20), "Write SMS")
        self.bottom_widget_elements['sms_number_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 170, 400, 20), "Enter receiver number:")
        self.bottom_widget_elements['sms_number_line'] = \
            GUIElements.add_line_edit(self.bottom_widget, QtCore.QRect(10, 190, 160, 20), "SMSNumberLine")
        self.bottom_widget_elements['sms_message_lbl'] = \
            GUIElements.add_lbl(self.bottom_widget, QtCore.QRect(10, 210, 400, 20), "Write your message:")
        self.bottom_widget_elements['sms_message_line'] = \
            GUIElements.add_line_edit(self.bottom_widget, QtCore.QRect(10, 230, 160, 120), "SMSMessageLine")
        self.bottom_widget_elements['send_sms_btn'] = \
            GUIElements.add_push_btn(self.bottom_widget, QtCore.QRect(10, 350, 100, 20), "SendSMSBtn", "Send")

    def send_command(self):
        cmd = self.bottom_widget_elements['command_line'].text()
        if cmd:
            self.bottom_widget_elements['command_line'].clear()
            self.device_manager.send_command(cmd)

    def send_ussd(self):
        ussd = self.bottom_widget_elements['ussd_line'].text()
        if ussd:
            self.bottom_widget_elements['ussd_line'].clear()
            self.device_manager.send_command('AT+CUSD=1,"{}"'.format(ussd))

    def send_sms(self):
        number = self.bottom_widget_elements['sms_number_line'].text()
        message = self.bottom_widget_elements['sms_message_line'].text()
        if number and message:
            self.bottom_widget_elements['sms_number_line'].clear()
            self.bottom_widget_elements['sms_message_line'].clear()
            self.device_manager.send_command('AT+CMGF=1')
            time.sleep(1)
            self.device_manager.send_command('AT+CMGS="{}"'.format(number))
            time.sleep(1)
            self.device_manager.send_sms_message(message)

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

    def update_devices_combo_box(self, devices):
        self.head_widget_elements['chose_device_combo'].clear()
        self.head_widget_elements['chose_device_combo'].addItems(devices)
        self.footer_widget_elements['status_lbl'].setText("device discovery finished")
        self.head_widget_elements['discover_serial_btn'].setEnabled(True)
        self.head_widget_elements['connection_btn'].setEnabled(True)

    def update_selected_device_lbl(self, selected_device):
        self.head_widget_elements['selected_device_lbl'].setText("Selected device: {}".format(selected_device))
