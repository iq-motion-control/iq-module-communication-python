from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator


class HyperdriveSpeedModule(IqModule):
    """ Creates HyperdriveSpeedModule object which subclasses IqModule

    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule

    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    _DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"
    _MODULE_FILE_NAME = "hyperdrive_speed.json"
    def __init__(self, com: Communicator, module_id, use_hyperdrive: bool= True):
        super().__init__(com=com, module_idn=module_id, use_hyperdrive=use_hyperdrive)
