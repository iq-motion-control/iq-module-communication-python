from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.iq_devices.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.communicator import Communicator
from iqmotion.clients import client_with_entries
from iqmotion.custom_errors import IqModuleError
from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMaker
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.message_making.client_with_entries_message import ClientWithEntriesMessage


import time


class StepDirModule(IqModule):
    """ Creates StepDirModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
    """

    _MODULE_FILE_NAME = "step_direction.json"
