from iqmotion.communication.iq_module_abstract import IqModuleAbstract
from iqmotion.communication.client import Client
from iqmotion.communication.custom_error import IqModuleError as IqModuleError

import json
import os
import sys


class IqSpeedModule(IqModuleAbstract):
    _module_file_name = "iq2306_2200kv.json"

    def __init__(self):
        super(IqSpeedModule, self).__init__(self._module_file_name)

    def set(self, client: str, client_entry: str, args=None):
        if client not in self._clients_dict.keys():
            raise IqModuleError("Client not in IqModule")

        client = self._clients_dict[client]
        client.set(client_entry, args)

        return

    def get(self, client: str, client_entry: str):
        pass

    def save(self, client: str, client_entry: str):
        pass

    def list(self, client: str):
        client = self._clients_dict[client]
        client.list()

        return
