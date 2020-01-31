class ClientError(Exception):
    err_type = "CLIENT ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class CommunicationError(Exception):
    err_type = "COMMUNICATION ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class PacketQueueError(Exception):
    err_type = "PACKET QUEUE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class PacketStateError(Exception):
    err_type = "PACKET STATE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class IqModuleError(Exception):
    err_type = "IQ MODULE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class MessageMakerError(Exception):
    err_type = "MESSAGE MAKER ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"
