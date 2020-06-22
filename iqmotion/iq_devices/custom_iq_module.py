import os

from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator


class CustomIqModule(IqModule):
    _MODULE_FILE_NAME = ""

    def __init__(
        self,
        custom_module_location: str,
        com: Communicator,
        module_idn=0,
        extra_clients=None,
    ):
        module_file_path = os.path.join(
            os.path.dirname(custom_module_location),
            ("module_files/" + self._MODULE_FILE_NAME),
        )

        super().__init__(com, module_idn, extra_clients, module_file_path)

        if "extra_clients" in self._module_file_dict:
            for extra_client_name in self._module_file_dict["extra_clients"]:
                extra_client_file_path = os.path.join(
                    os.path.dirname(custom_module_location),
                    (f"extra_client_files/{extra_client_name}.json"),
                )
                self.add_client(extra_client_file_path)
