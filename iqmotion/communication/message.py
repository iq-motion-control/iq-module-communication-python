from iqmotion.communication.message_maker import MessageMaker

from abc import ABC, abstractmethod


class Message(ABC):

    def __init__(self, message_maker: MessageMaker):
        self._message_maker = message_maker

    @abstractmethod
    def make_bytes(self):
        """ this property is too abstract to understand. """
