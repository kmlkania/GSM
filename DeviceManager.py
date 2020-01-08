from threading import Thread
from SerialDevice import getSerialDevices, SerialGSMConnection


class DeviceManager:
    def __init__(self, gui_widget):
        self.devices = []
        self.selected_device = None
        self.serial_conn = None
        self.gui_widget = gui_widget

    def set_serial_devices(self):
        self.gui_widget.head_widget_elements['discover_serial_btn'].setEnabled(False)
        self.gui_widget.head_widget_elements['connection_btn'].setEnabled(False)
        self.selected_device = None
        self._close_connection()
        self.gui_widget.footer_widget_elements['status_lbl'].setText("device discovery started")
        thread1 = Thread(target=self.discover_devices_in_bg)
        thread1.start()

    def discover_devices_in_bg(self):
        self.gui_widget.head_widget_elements['chose_device_combo'].clear()
        self.devices = getSerialDevices()
        self.devices.reverse()
        self.gui_widget.head_widget_elements['chose_device_combo'].addItems([dev.__str__() for dev in self.devices])
        self.gui_widget.footer_widget_elements['status_lbl'].setText("device discovery finished")
        self.gui_widget.head_widget_elements['discover_serial_btn'].setEnabled(True)
        self.gui_widget.head_widget_elements['connection_btn'].setEnabled(True)

    def update_selected_device_lbl(self, index):
        self.selected_device = self.devices[index].device
        self.gui_widget.head_widget_elements['selected_device_lbl'].setText("Selected device: {}".format(
            self.selected_device))

    def change_connection(self):
        if self.serial_conn:
            self._close_connection()
        else:
            self._open_connection()

    def _close_connection(self):
        if self.serial_conn:
            self.serial_conn = None
            self.gui_widget.head_widget_elements['connection_btn'].setText("Connect")
            self.gui_widget.footer_widget_elements['status_lbl'].setText("device disconnected")
            self.gui_widget.head_widget_elements['chose_device_combo'].setEnabled(True)
            self.gui_widget.footer_widget_elements['status_lbl'].setText("connection closed")
            self.gui_widget.bottom_widget.setEnabled(False)

    def _open_connection(self):
        if not self.serial_conn:
            self.serial_conn = SerialGSMConnection(self.selected_device)
            success, reason = self.serial_conn.establish_connection()
            if success:
                self.gui_widget.head_widget_elements['connection_btn'].setText("Disconnect")
                self.gui_widget.head_widget_elements['chose_device_combo'].setEnabled(False)
                self.gui_widget.footer_widget_elements['status_lbl'].setText("connection established with {}".format(
                    self.selected_device))
                self.gui_widget.bottom_widget.setEnabled(True)
                thread1 = Thread(target=self.gui_widget.update_cmd_monitor_list)
                thread1.start()
            else:
                self.serial_conn = None
                self.gui_widget.pop_up_alert("ERROR", reason)

    @property
    def has_active_connection(self):
        return True if self.serial_conn else False

    def get_data_from_device(self):
        return self.serial_conn.receive_data()

    def send_command(self, cmd):
        self.serial_conn.send_text_data(cmd)
