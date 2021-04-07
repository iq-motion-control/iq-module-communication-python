from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator
from iqmotion.custom_errors import IqModuleError

# This is a IQ Module Wrapper for the fortiq
# This Wrapper takes in firmware argument and creates an fortiq API Object
class Fortiq(IqModule):
    """ Creates fortiq object with default speed firmware
    
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
        module_idn: int = 0,
        firmware: str = "servo",  # Default Firmware 
        clients_path: str = None
    ):

        # Point to the correct JSON File depending on the firmware
        #
        if firmware.lower() == "speed":
            self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
            self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
            self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

            self._MODULE_FILE_NAME = "speed.json"

        elif firmware.lower() == "stepdir":
            self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
            self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
            self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

            self._MODULE_FILE_NAME = "step_direction.json"

        elif firmware.lower() == "servo": 
            self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
            self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
            self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

            self._MODULE_FILE_NAME = "servo.json"


        else:
            raise IqModuleError("'" + str(firmware) + "' firmware os not supported")

        # Pass the Super
        super().__init__(com, module_idn, clients_path)