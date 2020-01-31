from abc import ABC, abstractmethod


class MessageMaker(ABC):
    """ MessageMaker is the interface class used by the implementations of the bridge pattern.
    Each Implementations define how to make a message
    """

    @abstractmethod
    def make(self):
        """ this property is too abstract to understand. """
