from DeviceManager import DeviceManager
import mock


def test_device_manager_can_be_started():
    with mock.patch('GUIWidgets.GUIWidget') as gui_widget:
        dev = DeviceManager(gui_widget())
        assert isinstance(dev, DeviceManager)
