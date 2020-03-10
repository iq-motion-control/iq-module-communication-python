from iqmotion.communication.serial_packet_states import SerialStartState
from iqmotion.communication.serial_packet_states import SerialLenState
from iqmotion.communication.serial_packet_states import SerialTypeState
from iqmotion.communication.serial_packet_states import SerialPayloadState
from iqmotion.communication.serial_packet_states import SerialCrcState
from iqmotion.communication.crc import Crc
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.custom_errors import PacketStateError


from iqmotion.tests.helpers import make_fake_packet

import pytest


@pytest.fixture(params=[[1, 2, 3, 4, 5], []])
def circular_queue_with_packet(request):
    packet = make_fake_packet(request.param)
    cq = CircularQueue.from_iterable(packet)

    return [cq, packet]


class TestSerialStartState:
    def test_no_packet(self):
        data = [1, 2, 3, 4, 5]
        cq = CircularQueue.from_iterable(data)

        state = SerialStartState(cq)

        state.parse()

        assert state.find_next_state() == state

    def test_packet(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]

        state = SerialStartState(cq)

        state.parse()

        assert type(state.find_next_state()) == SerialLenState


class TestSerialLenState:
    def test_wrong_parse_index(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        len_data = len(circular_queue_with_packet[1])
        parse_index = len_data + 1

        state = SerialLenState(cq, 0, parse_index, 0)
        state.parse()

        assert state.find_next_state() == state

    def test_packet(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]

        state = SerialStartState(cq)
        state.parse()
        state = state.find_next_state()

        state.parse()

        assert type(state.find_next_state()) == SerialTypeState

    def test_overflow_packet(self):
        packet = []
        for i in range(256):
            packet.append(i)

        packet[1] = 256

        cq = CircularQueue.from_iterable(packet)
        state = SerialLenState(cq)

        with pytest.raises(PacketStateError) as err:
            state.parse()

        err_str = err.value.message
        assert (
            "PACKET STATE ERROR: Packet overflow, message is bigger than 256 bytes\n"
            == err_str
        )


class TestSerialTypeState:
    def test_wrong_parse_index(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        len_data = len(circular_queue_with_packet[1])
        parse_index = len_data + 1

        state = SerialTypeState(cq, 0, parse_index, 0)
        state.parse()

        assert state.find_next_state() == state

    def test_packet(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        payload_len = circular_queue_with_packet[1][1]

        state = SerialStartState(cq)
        state.parse()

        for _ in range(2):
            state = state.find_next_state()
            state.parse()

        new_state_type = type(state.find_next_state())

        if payload_len == 0:
            assert new_state_type == SerialCrcState
        else:
            assert new_state_type == SerialPayloadState


class TestSerialPayloadState:
    def test_wrong_parse_index(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        len_data = len(circular_queue_with_packet[1])
        parse_index = len_data + 1

        state = SerialPayloadState(cq, 0, parse_index, 5)
        state.parse()

        assert state.find_next_state() == state

    def test_packet(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]

        state = SerialStartState(cq)
        state.parse()

        for _ in range(3):
            state = state.find_next_state()
            state.parse()

        assert type(state.find_next_state()) == SerialCrcState


class TestSerialCrcState:
    def test_no_crc(self):
        data = [1, 2, 3, 4, 5]
        cq = CircularQueue.from_iterable(data)

        state = SerialCrcState(cq)
        state.parse()

        assert state.is_succesful == False

    def test_crc_state_packet(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        message = circular_queue_with_packet[1][2:-2]

        state = SerialStartState(cq)
        state.parse()

        for _ in range(4):
            state = state.find_next_state()
            state.parse()

        assert state.message == message

    def test_wrong_parse_index(self, circular_queue_with_packet):
        cq = circular_queue_with_packet[0]
        len_data = len(circular_queue_with_packet[1])
        parse_index = len_data + 1

        state = SerialCrcState(cq, 0, parse_index, 0)
        state.parse()

        assert state.is_succesful == False
