from GUIMainWindow import GUIMainWindow
from PyQt5 import QtCore
import mock
import pytestqt


def test_main_window_search_button_clicked(qtbot):
    with mock.patch('DeviceManager.DeviceManager.__init__', return_value=None):
        with mock.patch('DeviceManager.DeviceManager.set_serial_devices') as search_devices:
            window = GUIMainWindow()
            window.setup_window()
            qtbot.mouseClick(window.gui_widget.head_widget_elements['discover_serial_btn'], QtCore.Qt.LeftButton)
            search_devices.assert_called_once()

