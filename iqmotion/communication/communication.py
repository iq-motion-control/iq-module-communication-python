from abc import ABC, abstractmethod


class Communication(ABC):

    @abstractmethod
    def send_message(self, message: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def add_to_send_queue(self, bytes: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def send_now(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def read_bytes(self):
        """ this property is too abstract to understand. """

    @property
    @abstractmethod
    def bytes_left_in_queue(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def extract_message(self):
        """ this property is too abstract to understand. """
