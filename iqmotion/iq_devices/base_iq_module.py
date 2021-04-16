from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator


class BaseIqModule(IqModule):
    _MODULE_FILE_NAME = "base.json"

    def __init__(
        self,
        com: Communicator,
        module_idn: int = 0,
        clients_path: str = None,
    ):

        super().__init__(com, module_idn, clients_path)
