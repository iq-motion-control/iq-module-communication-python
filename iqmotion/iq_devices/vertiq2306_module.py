from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator
from iqmotion.custom_errors import IqModuleError


class Vertiq2306(IqModule):
    def __init__(
        self,
        com: Communicator,
        module_idn: int = 0,
        firmware: str = "speed",  # Default Firmware
        clients_path: str = None,
    ):
        """Creates Vertiq2306 object with default speed firmware.

        :param com: The communicator object used to interface with the IqModule
        :type com: Communicator
        :param module_idn: The idn of the module (default: 0)
        :type module_idn: int
        :param firmware: The firmware type used to determine which clients are available for the module to use
            Options include:
                * speed
                * stepdir
                * servo
                * pulsing
        :type firmware: str
        :param clients_path: Optional parameter to specify a directory containing extra clients for the module to use (default: {None})
        :type clients_path: str
        """

        # Point to the correct JSON File depending on the firmware
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

        elif firmware.lower() == "pulsing":
            self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
            self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
            self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

            self._MODULE_FILE_NAME = "pulsing.json"

        else:
            raise IqModuleError("'" + str(firmware) + "' firmware is not supported")

        # Pass the Super
        super().__init__(com, module_idn, clients_path)
