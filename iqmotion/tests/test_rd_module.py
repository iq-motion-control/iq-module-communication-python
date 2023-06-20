import pytest
from unittest.mock import Mock, patch

from serial.serialutil import SerialException

from iqmotion.iq_devices.rd_iq_module import RdModule
from iqmotion.tests.helpers import DummySerial, MockCommunicator
from iqmotion.custom_errors import CommunicationError, IqModuleError


class TestRdModule:
    
    # Test Bad Port Name
    def test_bad_port_name(self):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB1"]))

        with patch("serial.Serial") as mock_class:
            mock_class.side_effect = SerialException
            with pytest.raises(CommunicationError):
                RdModule("/dev/ttyUSB0")

    # Test autoconnection with 1 serial port available
    # Testing autoconnection to a speed and position module
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_mock_one_port(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0"]))
        setattr(RdModule, "get", Mock(side_effect=[0x100000, 0x200000]))
        mock_serial.return_value = MockCommunicator()
        mot = RdModule()
        assert(mot._DEFAULT_CONTROL_CLIENT == "propeller_motor_control")

    # Test autoconnection with multiple serial ports available
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_mock_mult_ports(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0", "/dev/ttyUSB1"]))
        mock_serial.return_value = MockCommunicator()
        with pytest.raises(CommunicationError):
            RdModule()

    # Test no serial ports available
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_mock_no_ports(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=[]))
        mock_serial.return_value = MockCommunicator()
        with pytest.raises(CommunicationError):
            RdModule()

    # Test autoconnection with 1 serial port available but unknown firmware style
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_mock_one_port(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0"]))
        setattr(RdModule, "get", Mock(side_effect=[0x12300000]))
        mock_serial.return_value = MockCommunicator()
        with pytest.raises(IqModuleError):
            RdModule()