from iqmotion.communication.message import Message


class ClientWithEntriesMessage(Message):

    def make_bytes(self):
        return self._message_maker.make()
