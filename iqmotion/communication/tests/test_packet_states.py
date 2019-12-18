from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.crc import Crc
from iqmotion.communication.packet_states import StartState
from iqmotion.communication.packet_states import LenState
from iqmotion.communication.packet_states import TypeState
from iqmotion.communication.packet_states import DataState
from iqmotion.communication.packet_states import CrcState

import pytest


def make_fake_message(data):
    data_type = 0
    data_len = len(data)

    start = 0x55

    crc_data = [data_len, data_type]
    crc_data.extend(data)
    crc = Crc.make_crc(crc_data)
    crcl = crc & 0xff
    crch = crc >> 8

    fake_message = [start, data_len, data_type]
    fake_message.extend(data)
    fake_message.append(crcl)
    fake_message.append(crch)

    # print(fake_message)

    return bytearray(fake_message)


class TestStartState():

    def test_start_state_no_packet(self):
        data = [1, 2, 3, 4, 5]

        circular_queue = CircularQueue.from_iterable(data)
        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        assert state.find_next_state() == state

    def test_start_state_packet(self):
        data = [1, 2, 3, 4, 5]
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        assert type(state.find_next_state()) == LenState


class TestLenState():

    def test_len_state_no_packet(self):
        data = [1, 2, 3, 4, 5]

        circular_queue = CircularQueue.from_iterable(data)
        state = LenState(circular_queue, 0, 6, 0)
        state.parse()

        assert state.find_next_state() == state

    def test_len_state_packet(self):
        data = [1, 2, 3, 4, 5]
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        state = state.find_next_state()
        state.parse()

        assert type(state.find_next_state()) == TypeState


class TestTypeState():

    def test_type_state_no_packet(self):
        data = [1, 2, 3, 4, 5]

        circular_queue = CircularQueue.from_iterable(data)
        state = TypeState(circular_queue, 0, 6, 0)
        state.parse()

        assert state.find_next_state() == state

    def test_type_state_packet_with_data(self):
        data = [1, 2, 3, 4, 5]
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        for _ in range(2):
            state = state.find_next_state()
            state.parse()

        assert type(state.find_next_state()) == DataState

    def test_type_state_packet_without_data(self):
        data = []
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        for _ in range(2):
            state = state.find_next_state()
            state.parse()

        assert type(state.find_next_state()) == CrcState


class TestDataState():

    def test_data_state_no_packet(self):
        data = [1, 2, 3, 4, 5]

        circular_queue = CircularQueue.from_iterable(data)
        state = DataState(circular_queue, 0, 6, 5)
        state.parse()

        assert state.find_next_state() == state

    def test_data_state_packet(self):
        data = [1, 2, 3, 4, 5]
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        for _ in range(3):
            state = state.find_next_state()
            state.parse()

        assert type(state.find_next_state()) == CrcState


class TestCrcState():

    def test_crc_state_no_packet(self):
        data = [1, 2, 3, 4, 5]

        circular_queue = CircularQueue.from_iterable(data)
        state = CrcState(circular_queue, 0, 0, 0)
        state.parse()

        assert state.succesful == 0

    def test_crc_state_packet(self):
        data = [1, 2, 3, 4, 5]
        fake_message = make_fake_message(data)
        circular_queue = CircularQueue.from_iterable(fake_message)

        state = StartState(circular_queue, 0, 0, 0)
        state.parse()

        for _ in range(4):
            state = state.find_next_state()
            state.parse()

        assert type(state.find_next_state()) == CrcState
