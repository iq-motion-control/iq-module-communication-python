from abc import ABC, abstractmethod


class Client(ABC):

    @abstractmethod
    def read_message(self, message: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def is_fresh(self, value_name: str = ""):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_reply(self, value_name: str = ""):
        """ this property is too abstract to understand. """
