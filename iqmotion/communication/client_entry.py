from abc import ABC, abstractmethod


class ClientEntry(ABC):

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
