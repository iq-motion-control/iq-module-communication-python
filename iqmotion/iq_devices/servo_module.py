from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.iq_devices.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.communicator import Communicator
from iqmotion.clients import client_with_entries
from iqmotion.custom_errors import IqModuleError
from iqmotion.message_making.dictionary_message_maker import DictionaryMessageMaker
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.message_making.client_with_entries_message import ClientWithEntriesMessage


import time


class ServoModule(IqModule):
    """ ServoModule is an implementation of IqModule

    It defines how to communicate to a module that is using the servo firwmare
    """
    _MODULE_FILE_NAME = "servo.json"
