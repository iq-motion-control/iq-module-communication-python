import os

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

        # if "extra_clients" in self._module_file_dict:
        #     for extra_client_name in self._module_file_dict["extra_clients"]:
        #         extra_client_file_path = os.path.join(
        #             os.path.dirname(custom_module_location),
        #             (f"extra_client_files/{extra_client_name}.json"),
        #         )
        #         self.add_client(extra_client_file_path)
