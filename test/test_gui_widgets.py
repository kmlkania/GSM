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


def test_button_search_clicked(qtbot, widget, QtCore):
    with mock.patch('DeviceManager.DeviceManager.set_serial_devices') as search_devices:
        widget.setup_actions()
        qtbot.mouseClick(widget.head_widget_elements['discover_serial_btn'], QtCore.Qt.LeftButton)
        search_devices.assert_called_once()


def test_no_connection_attempt_when_inactive_connection_btn_clicked(qtbot, widget, QtCore):
    with mock.patch('DeviceManager.DeviceManager.set_serial_devices'):
        with mock.patch('DeviceManager.DeviceManager.change_connection') as connection_change:
            widget.setup_actions()
            qtbot.mouseClick(widget.head_widget_elements['connection_btn'], QtCore.Qt.LeftButton)
            connection_change.assert_not_called()


def test_connection_can_be_established(qtbot, widget, QtCore):
    with mock.patch('DeviceManager.DeviceManager.set_serial_devices',
                    new_callable=widget.update_devices_combo_box(['COM1', 'COM5'])):
        with mock.patch('DeviceManager.DeviceManager.update_selected_device',
                        new_callable=widget.update_selected_device_lbl('COM1')):
            with mock.patch('DeviceManager.DeviceManager.change_connection') as connection_change:
                widget.setup_actions()
                qtbot.mouseClick(widget.head_widget_elements['discover_serial_btn'], QtCore.Qt.LeftButton)
                qtbot.mouseClick(widget.head_widget_elements['connection_btn'], QtCore.Qt.LeftButton)
                connection_change.assert_called_once()
                assert widget.head_widget_elements['selected_device_lbl'].text() == 'Selected device: COM1'


@pytest.fixture
def widget(qtbot):
    from PyQt5 import QtWidgets
    with mock.patch('DeviceManager.DeviceManager.__init__', return_value=None):
        widget = GUIWidget(QtWidgets.QMainWindow())
        widget.setup_head_widget()
        widget.setup_bottom_widget()
        widget.setup_footer_widget()
        return widget


@pytest.fixture
def QtCore():
    from PyQt5 import QtCore
    return QtCore



