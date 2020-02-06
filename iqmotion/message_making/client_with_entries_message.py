from iqmotion.message_making.message import Message


class ClientWithEntriesMessage(Message):
    """ ClientWithEntrisMessage is an implementation of the Message class
    It specifizes how the ClientWithEntries class makes messages
    """

    def make_bytes(self):
        """ Call the correct MessageMaker to make a message

        Returns:
            bytearray: message
        """
        return self._message_maker.make()
