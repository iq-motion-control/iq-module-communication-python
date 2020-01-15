from iqmotion.communication.client import Client
from iqmotion.communication.communication import Communication
from iqmotion.communication.custom_error import ClientError
from iqmotion.communication.dictionary_client_entry import DictionaryClientEntry
from iqmotion.communication.process_client_entry import ProcessClientEntry

import os
import json


class ClientWithEntries(Client):

    def __init__(self, client_file_name: str, module_idn=0):

        self._client_entry_dict = {}
        self._com = Communication
        self._module_idn = module_idn

        client_file = self._parse_client_json(client_file_name)

        self._populate_client_entries(client_file)

    def _parse_client_json(self, client_file_name: str):
        client_json = client_file_name + ".json"

        file_path = os.path.join(
            os.path.dirname(__file__), ('clients/' + client_json))

        with open(file_path) as json_file:
            client_file = json.load(json_file)

        return client_file

    def _populate_client_entries(self, client_file: dict):
        for client_entry_data_dict in client_file:
            client_entry_name = client_entry_data_dict["param"]
            client_entry = self._create_client_entry(client_entry_data_dict)

            self._client_entry_dict[client_entry_name] = client_entry

        return

    def _create_client_entry(self, client_entry_data_dict: dict):

        # special case where no "payload_type" field exists, legacy compatibility
        if "payload_type" not in client_entry_data_dict.keys():
            client_entry = DictionaryClientEntry(client_entry_data_dict)
            return client_entry

        payload_type = client_entry_data_dict["payload_type"]

        if payload_type == 1:
            client_entry = ProcessClientEntry(client_entry_data_dict)
        else:
            raise ClientError(
                "ClientWithEntries does not support this payload type")

        return client_entry

    def read_message(self, message: bytearray):
        msg_type_idn = message[0]
        msg_param_idn = message[1]
        msg_value = message[3:]

        for client_entry in self._client_entry_dict.values():
            type_idn = client_entry.data.type_idn
            param_idn = client_entry.data.param_idn

            if (msg_type_idn == type_idn) & (msg_param_idn == param_idn):
                client_entry.value = msg_value

    def is_fresh(self, value_name: str = ""):
        client_entry = self._client_entry_dict[value_name]
        return client_entry.fresh

    def get_reply(self, value_name: str = ""):
        client_entry = self._client_entry_dict[value_name]
        return client_entry.value

    @property
    def module_idn(self):
        return self._module_idn

    @property
    def client_entries(self):
        return self._client_entry_dict
