from iqmotion.communication.iq_module_abstract import IqModuleAbstract
from iqmotion.communication.client import Client
from iqmotion.communication.custom_error import IqModuleError as IqModuleError
from iqmotion.communication.serial_communication import SerialCommunication

import json
import os
import sys


class IqSpeedModule(IqModuleAbstract):
    _module_file_name = "iq2306_2200kv.json"

    def __init__(self, com, module_idn=0):
        super(IqSpeedModule, self).__init__(
            self._module_file_name, module_idn)

        self._com = com

    def set(self, client: str, client_entry: str, args=None):
        if client not in self._clients_dict.keys():
            raise IqModuleError("Client not in IqModule")

        client = self._clients_dict[client]

        packet = client.make_set_packet(client_entry, args)

        self._com.send_packet(packet)

        return

    def get(self, client: str, client_entry: str):
        pass

    def save(self, client: str, client_entry: str):
        pass

    def list(self, client: str):
        client = self._clients_dict[client]
        client.list()

        return

    # TODO: add list_clients()
