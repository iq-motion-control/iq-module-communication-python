from abc import ABC, abstractmethod


class ClientEntry(ABC):
    """ClientEntry is an interface class in order to store and access the information expressed by an entry in a client file.
    """

    @abstractmethod
    def read_message(self, msg):
        """ this property is too abstract to understand. """

    @property
    @abstractmethod
    def fresh(self):
        """ this property is too abstract to understand. """

    @property
    @abstractmethod
    def value(self):
        """ this property is too abstract to understand. """

    @value.setter
    @abstractmethod
    def value(self, val):
        """ this property is too abstract to understand. """

    @property
    @abstractmethod
    def data(self):
        """ this property is too abstract to understand. """
