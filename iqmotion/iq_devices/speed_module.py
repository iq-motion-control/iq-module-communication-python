from iqmotion.iq_devices.iq_module import IqModule

import time


class SpeedModule(IqModule):
    """ Creates SpeedModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
    """

    _MODULE_FILE_NAME = "speed.json"
