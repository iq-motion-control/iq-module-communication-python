import os
import json

from iqmotion.clients.client import Client
from iqmotion.custom_errors import ClientError
from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntry


class ClientWithEntries(Client):
    """ ClientWithEntries is an implementation of Client
        A ClientWithEntries object is able to read a message to store its content if needed, check if it's fresh and retrieve it.

        A ClientWithEntries is defined by a .json file where all its entries data is located
    """

    def __init__(self, client_file_path: str, module_idn=0):
        self._client_entry_dict = {}
        self._module_idn = module_idn

        client_file = self._parse_client_json(client_file_path)

        self._populate_client_entries(client_file)

    @classmethod
    def from_default_clients(cls, client_file_name: str, module_idn=0):
        client_json = client_file_name + ".json"

        file_path = os.path.join(
            os.path.dirname(__file__), ("client_files/" + client_json)
        )

        return ClientWithEntries(file_path, module_idn)

    def _parse_client_json(self, client_file_path: str):

        with open(client_file_path) as json_file:
            client_file = json.load(json_file)

        return client_file

    def _populate_client_entries(self, client_file: dict):
        for client_entry_data_dict in client_file:
            client_entry_name = client_entry_data_dict["param"]
            client_entry = self._create_client_entry(client_entry_data_dict)

            self._client_entry_dict[client_entry_name] = client_entry

    def _create_client_entry(self, client_entry_data_dict: dict):
        # special case where no "payload_type" field exists, legacy compatibility
        if "payload_type" not in client_entry_data_dict.keys():
            client_entry = DictionaryClientEntry(client_entry_data_dict)
        else:
            raise ClientError("ClientWithEntries does not support this payload type")

        # UNCOMMENT WHEN YOU HANDLE PROCESS CLIENT ENTRY
        # payload_type = client_entry_data_dict["payload_type"]
        # if payload_type == 1:
        #     client_entry = ProcessClientEntry(client_entry_data_dict)
        # else:
        #     raise ClientError(
        #         "ClientWithEntries does not support this payload type")

        return client_entry

    def read_message(self, message: bytearray):
        """ Takes in a message and puts it in the right client entries by matching type_idns
        """
        msg_type_idn = message[0]

        for client_entry in self._client_entry_dict.values():
            type_idn = client_entry.data.type_idn

            if type_idn == msg_type_idn:
                client_entry.read_message(message)

    def is_fresh(self, value_name: str = ""):
        """ Checks if a specific client entry has a fresh value

        Args:
            value_name (String): Client entry name

        Returns:
            True: if value is fresh
            False: if value is not fres
        """
        client_entry = self._client_entry_dict[value_name]
        return client_entry.fresh

    def get_reply(self, value_name: str = ""):
        """ Gets the value from a specific client entry

        Args:
            value_name (String): Client entry name

        Returns:
            (format): value from the client entry with its type define by the format entry
        """
        client_entry = self._client_entry_dict[value_name]
        return client_entry.value

    @property
    def module_idn(self):
        """ Returns the module idn of the client

        Returns:
            int: module idn
        """
        return self._module_idn

    @property
    def client_entries(self):
        """ Returns a dictionary of client entries available in this client

        Returns:
            dict: dictonary of client entries {client_entry_name(String): ClienEntry}
        """
        return self._client_entry_dict
