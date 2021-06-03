import os

from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator


# There are 3 options when it comes to adding extra clients
#
#       -Quick and dirty-
#   1.  clients_path {str: directory path}:   
#           Points to a directory containing client entry jsons
#           Note: this option will add every client entry in the folder
# 
#       -More Work but Flexible-
#   2.  extra_clients {list: [dir path, dir path, ...]}:
#           Contains a list of paths to each cleint entry you want to include
#           Note: you need to pass in an absolute paths
#
#       -Most Work but cleanest-
#   3.  custom_module_location {str: directory path}:
#           Commonly passed in as a cwd path, this can contain a module file
#           in addition to extra client files. 
#           Note: You need to have a folder named extra_client_files hosting your 
#                 client files
#           Example of 3rd Option
#           {
#             "clients": [
#               "brushless_drive",
#               "propeller_motor_control",
#               "anticogging",
#               "buzzer_control",
#               "esc_propeller_input_parser",
#               "hobby_input",
#               "persistent_memory",
#               "power_monitor",
#               "serial_interface",
#               "servo_input_parser",
#               "step_direction_input",
#               "system_control",
#               "temperature_estimator",
#               "temperature_monitor_uc"
#             ],
#             "extra_clients": [
#               "extra_client"
#             ]
#           }


class CustomIqModule(IqModule):
    _MODULE_FILE_NAME = ""

    def __init__(
        self,
        custom_module_location: str,
        com: Communicator,
        module_idn=0,
        clients_path: str=None,
        extra_clients: list=None,
    ):
        module_file_path = os.path.join(
            os.path.dirname(custom_module_location),
            ("module_files/" + self._MODULE_FILE_NAME),
        )

        super().__init__(com, 
                        module_idn, 
                        clients_path=clients_path,
                        extra_clients=extra_clients, 
                        module_file_path=module_file_path)

        # This will pull clients from the Module JSON 
        #       --Refer to example Below--
        if "extra_clients" in self._module_file_dict:
            for extra_client_name in self._module_file_dict["extra_clients"]:
                extra_client_file_path = os.path.join(
                    os.path.dirname(custom_module_location),
                    (f"extra_client_files/{extra_client_name}.json"),
                )
                self.add_client(extra_client_file_path)


