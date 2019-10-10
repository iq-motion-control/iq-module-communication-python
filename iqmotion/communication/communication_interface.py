from abc import ABC, abstractmethod


class CommunicationInterface(ABC):

    @abstractmethod
    def Flush(self):
        pass

    @abstractmethod
    def GetBytes(self):
        pass

    @abstractmethod
    def PeekPacket(self):
        pass

    @abstractmethod
    def DropPacket(self):
        pass

    @abstractmethod
    def SendPacket(self, pkt):
        pass

    @abstractmethod
    def SendMsg(self, msg_spec, msg):
        pass

    @abstractmethod
    def UnpackMsg(self, msg_spec, pkt_data):
        pass
