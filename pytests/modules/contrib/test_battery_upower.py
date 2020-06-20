import pytest

import dbus
import core.config
import modules.contrib.battery_upower

@pytest.fixture
def upower_manager():
    return modules.contrib.battery_upower.UPowerManager()

def test_properties(upower_manager):
    assert upower_manager.UPOWER_NAME == "org.freedesktop.UPower"
    assert upower_manager.UPOWER_PATH == "/org/freedesktop/UPower"
    assert upower_manager.DBUS_PROPERTIES == "org.freedesktop.DBus.Properties"

def _mock_dbus_interface(mocker):
    upower_manager.bus = mocker.Mock()
    dbus.Interface = mocker.Mock()
    dbus.Interface.return_value = mocker.Mock()
    return dbus.Interface.return_value

def test_detect_devices(mocker, upower_manager):
    _mock_dbus_interface(mocker).EnumerateDevices = mocker.Mock()
    dbus.Interface.return_value.EnumerateDevices.return_value = ["str1", "str2"]
    assert upower_manager.detect_devices() == ["str1", "str2"]

def test_display_device(mocker, upower_manager):
    _mock_dbus_interface(mocker).GetDisplayDevice.return_value = "display"
    assert upower_manager.get_display_device() == "display"

def test_critical_action(mocker, upower_manager):
    _mock_dbus_interface(mocker).GetCriticalAction.return_value = "critical_action"
    assert upower_manager.get_critical_action() == "critical_action"
