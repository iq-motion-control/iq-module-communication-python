from abc import ABC, abstractmethod


class Client(ABC):
    """ Client is an interface class used by the different client implementations.
    A Client object is able to read a message to store its content if needed, check if it's fresh and retrieve it
    """

    @abstractmethod
    def read_message(self, message: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def is_fresh(self, value_name: str = ""):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get_reply(self, value_name: str = ""):
        """ this property is too abstract to understand. """
