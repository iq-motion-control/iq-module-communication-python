from abc import ABC, abstractmethod


class Communicator(ABC):
    """ Communicator is an interface class that enables different type of communication protocole
    implementations while keeping the same message structure for every device.
    It is the implementation's job to "package" the message into its own package as well as 
    extract messages from its own packaging scheme.
    """

    @abstractmethod
    def send_message(self, message: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def add_to_out_queue(self, out_bytes: bytearray):
        """ this property is too abstract to understand. """

    @abstractmethod
    def send_now(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def flush_input_buffer(self):
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
