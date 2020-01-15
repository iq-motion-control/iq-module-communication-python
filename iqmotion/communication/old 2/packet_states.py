
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.crc import Crc

from abc import abstractmethod


class PacketState():
    is_done = 0
    succesful = 0

    _parse_succesful = 0
    _message = []
    _start_index = 0
    _end_index = 0

    @abstractmethod
    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
        self._byte_queue = byte_queue
        self._start_index = start_index
        self._parse_index = parse_index
        self._packet_len = packet_len

    @abstractmethod
    def parse(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def find_next_state(self):
        """ this property is too abstract to understand. """

    def get_message(self):
        return self._message.copy()


class StartState(PacketState):
    _START_BYTE = 0x55

    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
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

        self.is_done = 1
        self.succesful = 0
        self._end_index = self._parse_index + 1

    def find_next_state(self):
        if self._parse_succesful:
            return LenState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class LenState(PacketState):
    _MAX_PACKET_SIZE = 10

    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            self._packet_len = self._byte_queue[self._parse_index+1]
            if self._packet_len < self._MAX_PACKET_SIZE:
                self._parse_index += 1
                self._parse_succesful = 1
            return
        except IndexError:
            self.is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
        return

    def find_next_state(self):
        if self._parse_succesful:
            return TypeState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class TypeState(PacketState):
    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            self._byte_queue[self._parse_index + 1]
            self._parse_index += 1
            self._parse_succesful = 1
            return
        except IndexError:
            self.is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
        return

    def find_next_state(self):
        if self._parse_succesful:
            if self._packet_len > 0:
                return DataState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
            else:
                return CrcState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class DataState(PacketState):
    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
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
            self.is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0

        return

    def find_next_state(self):
        if self._parse_succesful:
            return CrcState(self._byte_queue, self._start_index, self._parse_index, self._packet_len)
        else:
            return self


class CrcState(PacketState):
    def __init__(self, byte_queue: CircularQueue, start_index: int, parse_index: int, packet_len: int):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        try:
            crcl = self._byte_queue[self._parse_index + 1]
            crch = self._byte_queue[self._parse_index + 2]
            crc = (crch << 8) | crcl

            msg = self._extract_packet_message()
            expected_crc = Crc.make_crc(msg)

            if crc == expected_crc:
                self._message = msg.copy()
                self._end_index = self._parse_index + 3
                self.is_done = 1
                self.succesful = 1
            else:
                self.is_done = 1
                self.succesful = 0

        except IndexError:
            self.is_done = 1
            self._end_index = self._parse_index + 1
            self.succesful = 0

        return

    def find_next_state(self):
        return self

    def _extract_packet_message(self):
        msg_start = self._start_index + 1
        # the two is the Len and Type of the data
        msg_end = msg_start + self._parse_index
        msg = self._byte_queue[msg_start:msg_end]
        return msg
