from iqmotion.iq_devices.iq_module import IqModule


class ServoModule(IqModule):
    """ Creates ServoModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    _DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"

    _MODULE_FILE_NAME = "servo.json"
