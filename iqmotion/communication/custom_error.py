class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ClientError(Error):
    err_type = "CLIENT ERROR"

    def __init__(self, err_descriptor):
        self.message = self.err_type + ": " + err_descriptor + "\n"


class CommunicationError(Error):
    err_type = "COMMUNICATION ERROR"

    def __init__(self, err_descriptor):
        self.message = self.err_type + ": " + err_descriptor + "\n"


class PacketError(Error):
    err_type = "PACKET ERROR"

    def __init__(self, err_descriptor):
        self.message = self.err_type + ": " + err_descriptor + "\n"
