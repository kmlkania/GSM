from GUIWidgets import GUIWidget
import mock


def test_widget_can_be_started():
    with mock.patch('PyQt5.QtWidgets.QWidget') as qt_widget:
        with mock.patch('GUIMainWindow.GUIMainWindow') as main_window:
            widget = GUIWidget(main_window())
            assert isinstance(widget, GUIWidget)
