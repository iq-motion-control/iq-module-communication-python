
from ..client import Client


class BrushlessDriveClient(Client):

    def __init__(self, com, obj_id=0, timeout=0.2):
        filename = "brushless_drive.json"
        print(filename)
        super(BrushlessDriveClient, self).__init__(
            com, filename, obj_id, timeout)
