import copy

from iqmotion.communication.packet_state import PacketState
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.crc import Crc

from iqmotion.custom_errors import PacketStateError


def index_in_list(a_list, index):
    if index < len(a_list):
        return 1

    return 0


class SerialStartState(PacketState):
    """ SerialStartState defines the start state of a serial packet.
    It will parse the circular byte queue until it finds its start byte (0x55)
    """

    _START_BYTE = 0x55

    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):
        super().__init__(byte_queue, start_index, parse_index, packet_len)
        self._end_index = len(byte_queue)

    def parse(self):
        """ popleft every byte in the circular queue until it finds the start byte (0x55)
        """
        parse_index = self._start_index
        for _ in range(parse_index, self._end_index):
            if self._byte_queue[parse_index] == self._START_BYTE:
                self._parse_succesful = 1
                self._parse_index = parse_index
                return

            self._byte_queue.popleft()

        self._is_done = 1
        self._succesful = 0
        self._end_index = self._parse_index + 1

    def find_next_state(self):
        """ Finds next state depending on the success of parse

        Returns:
            next_state (SerialLenState): if parsing was successful
            next_state (SerialStartState): if parsing not successful
        """
        if self._parse_succesful:
            return SerialLenState(
                self._byte_queue, self._start_index, self._parse_index, self._packet_len
            )

        return self


class SerialLenState(PacketState):
    """ SerialLenState defines the Len state of a serial packet.
    It will parse the circular byte queue to find the Len Byte and store it in memory.
    Len Byte cannot be more than 250
    """

    _MAX_PACKET_SIZE = 255

    # pylint: disable=useless-super-delegation
    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        """ Find len byte and stores it in memory, if Len Byte > 250, raise an error

        Raise:
            PacketStateError: Packet overflow, message is bigger than 256 bytes
        """
        new_index = self._parse_index + 1
        if not index_in_list(self._byte_queue, new_index):
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
            return

        self._packet_len = self._byte_queue[new_index]
        if self._packet_len <= self._MAX_PACKET_SIZE:
            self._parse_index += 1
            self._parse_succesful = 1
        else:
            raise PacketStateError("Packet overflow, message is bigger than 256 bytes")

    def find_next_state(self):
        """ Finds next state depending on the success of parse 

        Returns:
            next_state (SerialTypeState): if parsing was successful
            next_state (SerialLenState): if parsing not successful
        """
        if self._parse_succesful:
            return SerialTypeState(
                self._byte_queue, self._start_index, self._parse_index, self._packet_len
            )

        return self


class SerialTypeState(PacketState):
    """ SerialTypeState defines the Type state of a serial packet.
    It will parse the circular byte queue to find the Type Byte.
    If the parsing was succesfull it will return SerialPayloadState if Len of payload > 0,
    otherwise it will skip SerialPayloadState and return SericalCrcState
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        """ Find Type byte
        """

        new_index = self._parse_index + 1
        if not index_in_list(self._byte_queue, new_index):
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._parse_succesful = 0
            return

        self._parse_index += 1
        self._parse_succesful = 1

    def find_next_state(self):
        """ Finds next state depending on the success of parse 

        Returns:
            next_state (SerialPayloadState): if parsing was successful and packet_len > 0
            next_state (SerialCrcState): if parsing was successful and packet_len = 0
            next_state (SerialTypeState): if parsing not successful
        """
        if self._parse_succesful:
            if self._packet_len > 0:
                return SerialPayloadState(
                    self._byte_queue,
                    self._start_index,
                    self._parse_index,
                    self._packet_len,
                )

            return SerialCrcState(
                self._byte_queue,
                self._start_index,
                self._parse_index,
                self._packet_len,
            )

        return self


class SerialPayloadState(PacketState):
    """ SerialPayloadState defines the Payload state of a serial packet.
    It will parse the circular byte queue to find all the payload bytes of the packet.
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):

        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        """ Find Paylod bytes
        """
        for ind in range(
            self._parse_index + 1, self._parse_index + 1 + self._packet_len
        ):
            # check if there is the right amount of bytes,
            if not index_in_list(self._byte_queue, ind):
                self._is_done = 1
                self._end_index = self._parse_index + 1
                self._parse_succesful = 0
                return

        self._parse_index += self._packet_len
        self._parse_succesful = 1

    def find_next_state(self):
        """ Finds next state depending on the success of parse 

        Returns:
            next_state (SerialCrcState): if parsing was successful
            next_state (SerialPayloadState): if parsing not successful
        """
        if self._parse_succesful:
            return SerialCrcState(
                self._byte_queue, self._start_index, self._parse_index, self._packet_len
            )

        return self


class SerialCrcState(PacketState):
    """ SerialCrcState defines the Crc state of a serial packet.
    It will check the current packet for the Crc bytes and verify that they are correct.
    If the Crc is correct, stores the message in its message @property
    """

    # pylint: disable=useless-super-delegation
    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):
        super().__init__(byte_queue, start_index, parse_index, packet_len)

    def parse(self):
        """ Find Crc bytes and check if they are correct.
        If correct, store message in its message @property
        """
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
                self._end_index = self._parse_index + 3
                self._pop_message_bytes()
                self._succesful = 0

        except IndexError:
            self._is_done = 1
            self._end_index = self._parse_index + 1
            self._succesful = 0

    def find_next_state(self):
        """ Finds next state depending on the success of parse 

        Returns:
            next_state (SerialCrcState): if parsing was successful
        """
        return self

    def _extract_packet_message(self):
        msg_start = self._start_index + 1
        # the two is the Len and Type of the data
        msg_end = msg_start + self._parse_index
        msg = bytearray(self._byte_queue[msg_start:msg_end])
        return msg

    def _pop_message_bytes(self):
        num_bytes_to_pop = self._end_index - self._start_index
        for _ in range(num_bytes_to_pop):
            self._byte_queue.popleft()
