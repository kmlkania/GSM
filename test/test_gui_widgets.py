from GUIWidgets import GUIWidget
import mock
import pytest
import pytestqt


def test_widget_can_be_started():
    with mock.patch('PyQt5.QtWidgets.QWidget'):
        with mock.patch('GUIMainWindow.GUIMainWindow') as main_window:
            with mock.patch('DeviceManager.DeviceManager'):
                widget = GUIWidget(main_window())
                assert isinstance(widget, GUIWidget)


@mock.patch('PyQt5.QtWidgets.QWidget')
@mock.patch('PyQt5.QtWidgets.QPushButton')
@mock.patch('PyQt5.QtWidgets.QLabel')
@mock.patch('PyQt5.QtWidgets.QComboBox')
@mock.patch('PyQt5.QtWidgets.QLineEdit')
@mock.patch('PyQt5.QtWidgets.QListWidget')
def test_widgets_setup(q_list, q_line, q_combo, q_lbl, q_btn, q_widget):
        with mock.patch('GUIMainWindow.GUIMainWindow') as main_window:
            with mock.patch('DeviceManager.DeviceManager'):
                widget = GUIWidget(main_window())
                widget.setup_head_widget()
                widget.setup_bottom_widget()
                widget.setup_footer_widget()
                assert widget.head_widget_elements
                assert widget.bottom_widget_elements
                assert widget.footer_widget_elements


def test_button_search_clicked(qtbot):
    from PyQt5 import QtCore, QtWidgets
    with mock.patch('DeviceManager.DeviceManager.__init__', return_value=None):
        with mock.patch('DeviceManager.DeviceManager.set_serial_devices') as search_devices:
            widget = GUIWidget(QtWidgets.QMainWindow())
            widget.setup_head_widget()
            widget.setup_bottom_widget()
            widget.setup_footer_widget()
            widget.setup_actions()
            qtbot.mouseClick(widget.head_widget_elements['discover_serial_btn'], QtCore.Qt.LeftButton)
            search_devices.assert_called_once()

