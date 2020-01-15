from iqmotion.communication.custom_error import CommunicationError

from abc import ABC, abstractmethod


class CommunicationAbsract():

    @abstractmethod
    def send_packet(self, packet_type, packet_data):
        """ this property is too abstract to understand. """
        return
