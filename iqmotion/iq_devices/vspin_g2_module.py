from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.communicator import Communicator


class VSpinG2Module(IqModule):
    """ Creates VSpinG2Module object which subclasses IqModule

    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule

    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    _DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"
    _MODULE_FILE_NAME = "vspin_g2.json"
    def __init__(self, com: Communicator, module_id: int = 0, clients_path: str = None):
        super().__init__(com=com, module_idn=module_id, clients_path=clients_path, use_vspin=True)
