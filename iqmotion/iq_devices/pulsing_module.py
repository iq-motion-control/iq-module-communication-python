from iqmotion.communication.communicator import Communicator
from iqmotion.iq_devices.custom_iq_module import CustomIqModule


class PulsingModule(CustomIqModule):
    """ Creates PulsingModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    _DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

    _MODULE_FILE_NAME = "pulsing.json"

    def __init__(
        self, com: Communicator, module_idn=0, extra_clients=None,
    ):
        super().__init__(__file__, com, module_idn, extra_clients)
