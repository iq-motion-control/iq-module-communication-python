from unittest.mock import patch, MagicMock, call

import pytest

from iqmotion.communication.serial_communicator import SerialCommunicator
from iqmotion.custom_errors import CommunicationError

from iqmotion.tests.helpers import DummySerial
from iqmotion.tests.helpers import make_fake_packet


class TestSerialCommunicator:
    @pytest.fixture
    def mock_serial(self, monkeypatch):
        # pylint: disable=unused-argument
        def mock_find_serial_port(*args, **kwargs):
            return ["test_port", "test_port2"]

        monkeypatch.setattr(
            SerialCommunicator, "_find_serial_port", mock_find_serial_port
        )

        with patch("serial.Serial") as mock_class:
            mock_class.return_value = DummySerial("test_port", 115200)
            mock_serial = mock_class.return_value

            yield mock_serial

    def test__init__wrong_port(self):
        SerialCommunicator._find_serial_port = MagicMock()
        SerialCommunicator._find_serial_port.return_value = ["test_port", "test_port2"]
        port_name = "wrong_port"
        with pytest.raises(CommunicationError) as err:
            SerialCommunicator(port_name)

        pretty_available_ports_str = '\t"test_port"\n\t"test_port2"\n'
        expected_err = f"COMMUNICATION ERROR: Serial port '{port_name}' is not available, here is a list of available ports:\n{pretty_available_ports_str}"

        err_str = err.value.message
        assert expected_err == err_str

    def test__del__(self, mock_serial):
        mock_serial.close = MagicMock()
        ser = SerialCommunicator("test_port")
        del ser

        assert mock_serial.close.called

    def test_send_now(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunicator("test_port")

        packet = bytearray([1, 2, 3, 4])
        ser.add_to_out_queue(packet)
        ser.send_now()
        assert mock_serial.write.call_args == call(packet)

    def test_send_now_empty_out_queue(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunicator("test_port")

        ser.send_now()
        assert mock_serial.write.call_args == call(bytearray([]))

    def test_send_message(self, mock_serial):
        mock_serial.write = MagicMock()
        ser = SerialCommunicator("test_port")

        message = bytearray([0, 11, 12, 13, 14])
        ser.send_message(message)

        packet = make_fake_packet(message[1:], 0)

        assert mock_serial.write.call_args == call(packet)

    def test_flush_input_buffer(self, mock_serial):
        # fake_message = bytearray([i for i in range(100)])
        packet = bytes([0, 1, 2, 3, 4])
        mock_serial.reset_input_buffer = MagicMock()
        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)

        ser = SerialCommunicator("test_port")
        ser.read_bytes()
        assert ser.bytes_left_in_queue

        ser.flush_input_buffer()

        assert mock_serial.reset_input_buffer.called
        assert not ser.bytes_left_in_queue

    @pytest.mark.parametrize(
        "test_input", [(bytes([0, 1, 2, 3, 4])), (bytearray([*range(255)]))],
    )
    def test_read_bytes(self, mock_serial, test_input):
        packet = test_input
        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser = SerialCommunicator("test_port")
        read_all_available = ser.read_bytes()

        assert mock_serial.read.call_args == call(len(packet))
        assert read_all_available

    def test_read_bytes_overflow(self, mock_serial):
        packet = bytes([10 for i in range(600)])
        mock_serial.read = MagicMock(return_value=packet[: (255 + 5) * 2])
        mock_serial._in_waiting = len(packet)

        ser = SerialCommunicator("test_port")
        read_all_available = ser.read_bytes()

        assert mock_serial.read.call_args == call((255 + 5) * 2)
        assert not read_all_available

    @pytest.mark.parametrize(
        "test_input", [(bytes([0, 1, 2, 3, 4])), (bytearray([*range(255)]))],
    )
    def test_byte_left_in_queue(self, mock_serial, test_input):
        packet = test_input
        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser = SerialCommunicator("test_port")
        ser.read_bytes()

        assert ser.bytes_left_in_queue

    # pylint: disable=unused-argument
    def test_byte_left_in_queue_empty(self, mock_serial):
        ser = SerialCommunicator("test_port")

        assert not ser.bytes_left_in_queue

    @pytest.mark.parametrize(
        "test_input", [(bytes([0, 1, 2, 3, 4])), (bytearray([*range(255)]))],
    )
    def test_extract_message(self, mock_serial, test_input):
        ser = SerialCommunicator("test_port")

        message = test_input
        packet = bytes(make_fake_packet(message, 0))

        mock_serial.read = MagicMock(return_value=packet)
        mock_serial._in_waiting = len(packet)
        ser.read_bytes()

        message_back = ser.extract_message()

        assert message_back[1:] == message

    def test_extract_message_from_empty_queue(self, mock_serial):
        ser = SerialCommunicator("test_port")

        message_back = ser.extract_message()

        assert message_back is None
