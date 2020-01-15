from iqmotion.communication.custom_error import PacketError

import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PayloadData:
    pass


class PayloadMakerAbstract():

    @abstractmethod
    def make_payload(self, payload_data):
        """ this property is too abstract to understand. """
