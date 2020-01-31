from abc import ABC, abstractmethod


class PacketQueue(ABC):
    """ PacketQueue is an interface class that enables extraction of well formed message from its circular byte queue

    It is a specialized circular queue which takes in raw bytes and returns the packet's message.
    The packet's message is a byte array consisting of a type byte followed by payload bytes.

    It is the implementation's job to parse the packet correctly (for that implementation) and return the packet's message"""

    @abstractmethod
    def put_bytes(self, new_bytes):
        """ this property is too abstract to understand. """

    @abstractmethod
    def peek(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def drop_packet(self):
        """ this property is too abstract to understand. """
