from abc import ABC, abstractmethod


class PacketQueue(ABC):
    @abstractmethod
    def put_bytes(self, new_bytes):
        """ this property is too abstract to understand. """

    @abstractmethod
    def peek(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def drop_packet(self):
        """ this property is too abstract to understand. """
