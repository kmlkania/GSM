from GUIWidgets import GUIWidget
import mock


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
def test_button_search_devices(q_list, q_line, q_combo, q_lbl, q_btn, q_widget):
        with mock.patch('GUIMainWindow.GUIMainWindow') as main_window:
            with mock.patch('DeviceManager.DeviceManager'):
                widget = GUIWidget(main_window())
                widget.setup_head_widget()
                widget.setup_bottom_widget()
                widget.setup_footer_widget()
                assert isinstance(widget, GUIWidget)
