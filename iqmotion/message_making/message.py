from abc import ABC, abstractmethod

from iqmotion.message_making.message_maker import MessageMaker


class Message(ABC):
    """ Message is the interface class used by the Specialiizations in a bridge pattern.
    Each implemenation should correspond to a different type of Clien implementation
    """

    def __init__(self, message_maker: MessageMaker):
        self._message_maker = message_maker

    @abstractmethod
    def make_bytes(self):
        """ this property is too abstract to understand. """
