from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator
from iqmotion.custom_errors import IqModuleError

# This is a IQ Module Wrapper for the vertiq 8108
# This Wrapper takes in firmware argument and creates an veritq8108 API Object
class vertiq8108(IqModule):
    """ Creates vertiq8108 object with default speed firmware
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
        firmware {str} -- Which firmware is the motor using (default: {"speed"})
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    def __init__(
        self,
        com: Communicator, 
        firmware = "speed",
        module_idn=0
    ):
        if firmware.lower() == "speed":
            self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
            self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
            self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

            self._MODULE_FILE_NAME = "speed.json"

            super().__init__(com,module_idn)
        else:
            raise IqModuleError("'" + str(firmware) + "' firmware is not supported")

        