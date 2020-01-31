from iqmotion.communication.serial_communication import SerialCommunication
from iqmotion.communication.crc import Crc
from iqmotion.communication.custom_error import CommunicationError

from iqmotion.communication.tests.helpers import DummySerial
from iqmotion.communication.tests.helpers import make_fake_packet

import pytest
import serial

from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestSerialCommunication:

    @pytest.fixture
    def mock_serial(self, monkeypatch):
        def mock_find_serial_port(*args, **kwargs):
            return ["test_port", "test_port2"]

        monkeypatch.setattr(SerialCommunication,
                            "_find_serial_port", mock_find_serial_port)

        with patch('serial.Serial') as mock_class:
            mock_class.return_value = DummySerial("test_port", 115200)
            mock_serial = mock_class.return_value

            yield mock_serial

    def test__init__wrong_port(self, mock_serial):
        with pytest.raises(CommunicationError) as err:
            SerialCommunication("wrong_port")

        pretty_available_ports_str = '\t"test_port"\n\t"test_port2"\n'
        expected_err = "COMMUNICATION ERROR: Serial port is not available, here is a list of available ports:\n" + \
            pretty_available_ports_str

        err_str = err.value.message
        assert expected_err == err_str

    def test__del__(self, mock_serial):
        mock_serial.close = MagicMock()
        ser = SerialCommunication('test_port')
        del ser

        assert mock_serial.close.called == True

    def test_send_now(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunication('test_port')

        packet = bytearray([1, 2, 3, 4])
        ser.add_to_out_queue(packet)
        ser.send_now()
        assert mock_serial.write.call_args == call(packet)

    def test_send_now_empty_out_queue(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunication('test_port')

        ser.send_now()
        assert mock_serial.write.call_args == call(bytearray([]))

    def test_send_message(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunication('test_port')

        message = bytearray([0, 11, 12, 13, 14])
        ser.send_message(message)

        packet = make_fake_packet(message[1:], 0)

        assert mock_serial.write.call_args == call(packet)

    def test_read_bytes(self, mock_serial):
        packet = bytes([0, 1, 2, 3, 4])
        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser = SerialCommunication('test_port')
        ser.read_bytes()

        assert mock_serial.read.call_args == call(len(packet))

    def test_byte_left_in_queue(self, mock_serial):
        packet = bytes([0, 1, 2, 3, 4])
        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser = SerialCommunication('test_port')
        ser.read_bytes()

        assert ser.bytes_left_in_queue == True

    def test_byte_left_in_queue_empty(self, mock_serial):
        ser = SerialCommunication('test_port')

        assert ser.bytes_left_in_queue == False

    def test_extract_message(self, mock_serial):
        ser = SerialCommunication('test_port')

        message = bytearray([0, 11, 12, 13, 14])
        packet = bytes(make_fake_packet(message[1:], 0))

        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser.read_bytes()

        message_back = ser.extract_message()

        assert message_back == message
