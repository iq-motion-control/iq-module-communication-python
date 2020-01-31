from iqmotion.iq_devices.iq_module import IqModule

import time


class SpeedModule(IqModule):
    """ SpeedModule is an implementation of IqModule

    It defines how to communicate to a module that is using the Speed firwmare
    """
    _MODULE_FILE_NAME = "speed.json"
