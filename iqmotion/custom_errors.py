class IqMotionError(Exception):
    """Base class for other custom exceptions"""

    message = ""


class ClientError(IqMotionError):
    err_type = "CLIENT ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class CommunicationError(IqMotionError):
    err_type = "COMMUNICATION ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class PacketQueueError(IqMotionError):
    err_type = "PACKET QUEUE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class PacketStateError(IqMotionError):
    err_type = "PACKET STATE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class IqModuleError(IqMotionError):
    err_type = "IQ MODULE ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"


class MessageMakerError(IqMotionError):
    err_type = "MESSAGE MAKER ERROR"

    def __init__(self, err_descriptor):
        super().__init__(err_descriptor)
        self.message = self.err_type + ": " + err_descriptor + "\n"
