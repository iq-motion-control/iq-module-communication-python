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
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_mock_one_port(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0"]))
        mock_serial.return_value = MockCommunicator()
        RdModule()

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

    # Test ramp velocity fails
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_ramp_velocity(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0"]))
        mock_serial.return_value = MockCommunicator()
        with pytest.raises(IqModuleError):
            module = RdModule()
            module.ramp_velocity(3,20)

    
    # Test ramp velocity fails
    @patch('iqmotion.iq_devices.rd_iq_module.SerialCommunicator')
    def test_ramp_prop_multi_velocity(self, mock_serial):
        setattr(RdModule, "_find_serial_ports", Mock(return_value=["/dev/ttyUSB0"]))
        mock_serial.return_value = MockCommunicator()
        module = RdModule()
        module.ramp_propeller_velocity(3,20)
        module.ramp_multi_turn_velocity(3,20)

    
