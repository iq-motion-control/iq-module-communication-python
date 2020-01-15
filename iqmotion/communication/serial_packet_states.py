from iqmotion.communication.packet_state import PacketState
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.crc import Crc

import copy


class SerialStartState(PacketState):
    _START_BYTE = 0x55

    def __init__(self, byte_queue: CircularQueue, start_index: int = 0, parse_index: int = 0, packet_len: int = 0):
        super().__init__(byte_queue, start_index, parse_index, packet_len)
        self._end_index = len(byte_queue)

    def parse(self):
        parse_index = self._start_index
        for _ in range(parse_index, self._end_index):
            if self._byte_queue[parse_index] == self._START_BYTE:
                self._parse_succesful = 1
                self._parse_index = parse_index
                return
            else:
                self._byte_queue.popleft()

        self._is_done = 1
        self._succesful = 0
        self._end_index = self._parse_index + 1

    def find_next_state(self):
        if self._parse_succesful:
            return SerialLenState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class SerialLenState(PacketState):
    _MAX_PACKET_SIZE = 10

    def __init__(self, byte_queue: CircularQueue, start_index: int = 0, parse_index: int = 0, packet_len: int = 0):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            self._packet_len = self._byte_queue[self._parse_index+1]
            if self._packet_len < self._MAX_PACKET_SIZE:
                self._parse_index += 1
                self._parse_succesful = 1
            return
        except IndexError:
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
        return

    def find_next_state(self):
        if self._parse_succesful:
            return SerialTypeState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class SerialTypeState(PacketState):

    def __init__(self, byte_queue: CircularQueue, start_index: int = 0, parse_index: int = 0, packet_len: int = 0):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            self._byte_queue[self._parse_index + 1]
            self._parse_index += 1
            self._parse_succesful = 1
            return
        except IndexError:
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
        return

    def find_next_state(self):
        if self._parse_succesful:
            if self._packet_len > 0:
                return SerialPayloadState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
            else:
                return SerialCrcState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class SerialPayloadState(PacketState):
    def __init__(self, byte_queue: CircularQueue, start_index: int = 0, parse_index: int = 0, packet_len: int = 0):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            for ind in range(self._parse_index+1, self._parse_index+1+self._packet_len):
                # check if there is the right amount of bytes,
                self._byte_queue[ind]
            self._parse_index += self._packet_len
            self._parse_succesful = 1
            return

        except IndexError:
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0

        return

    def find_next_state(self):
        if self._parse_succesful:
            return SerialCrcState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class SerialCrcState(PacketState):
    def __init__(self, byte_queue: CircularQueue, start_index: int = 0, parse_index: int = 0, packet_len: int = 0):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            crcl = self._byte_queue[self._parse_index + 1]
            crch = self._byte_queue[self._parse_index + 2]
            crc = (crch << 8) | crcl

            msg = self._extract_packet_message()
            expected_crc = Crc.make_crc(msg)

            if crc == expected_crc:
                self._message = copy.deepcopy(msg[1:])
                self._end_index = self._parse_index + 3
                self._is_done = 1
                self._succesful = 1
            else:
                self._is_done = 1
                self._succesful = 0

        except IndexError:
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._succesful = 0

        return

    def find_next_state(self):
        return self

    def _extract_packet_message(self):
        msg_start = self._start_index + 1
        # the two is the Len and Type of the data
        msg_end = msg_start + self._parse_index
        msg = bytearray(self._byte_queue[msg_start:msg_end])
        return msg
