from abc import ABC, abstractmethod
import copy

from iqmotion.communication.circular_queue import CircularQueue


class PacketState(ABC):
    """ PacketState is an abstract class that defines the state of a packet while parsing using a State Pattern. 
    It enables to parse the packet at the current state/position and find the next state depending on the current one
    until it eventually finds a whole packet and saves the message from the packet in its @property message

    It is the job of the implimentations to decide how to parse and find the next state
    """

    @abstractmethod
    def __init__(
        self,
        byte_queue: CircularQueue,
        start_index: int = 0,
        parse_index: int = 0,
        packet_len: int = 0,
    ):
        self._byte_queue = byte_queue
        self._start_index = start_index
        self._parse_index = parse_index
        self._packet_len = packet_len

        self._is_done = False
        self._succesful = False

        self._parse_succesful = False
        self._message = bytearray([])
        self._end_index = 0

    @property
    def is_done(self):
        return self._is_done

    @property
    def is_succesful(self):
        return self._succesful

    @property
    def message(self):
        return copy.deepcopy(self._message)

    @abstractmethod
    def parse(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def find_next_state(self):
        """ this property is too abstract to understand. """
