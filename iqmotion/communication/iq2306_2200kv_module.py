from iqmotion.communication.iq_module import IqModule
from iqmotion.communication.iq_module_json_parser import IqModuleJsonParser
from iqmotion.communication.communication import Communication
from iqmotion.communication.client_with_entries import ClientWithEntries
from iqmotion.communication.custom_error import IqModuleError
from iqmotion.communication.dictionary_message_maker import DictionaryMessageMaker
from iqmotion.communication.client_with_entries_message import ClientWithEntriesMessage

from iqmotion.communication.dictionary_client_entry import AccessType


import time


class Iq2306_2200kvModule(IqModule):
    _MODULE_FILE_NAME = "iq2306_2200kv.json"

    def __init__(self, com: Communication, module_idn=0):
        self._client_dict = {}
        self._com = com
        self._module_idn = module_idn

        module_file_dict = IqModuleJsonParser.parse(self._MODULE_FILE_NAME)
        self._create_clients(module_file_dict)

    def _create_clients(self, module_file_dict: dict):
        # TODO: parse different clients ?
        for client_name in module_file_dict["clients"]:
            self._client_dict[client_name] = ClientWithEntries(
                client_name, self._module_idn)

    def set(self, client_name: str, client_entry_name: str, *args):
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        if client_entry.data.format == "":
            raise IqModuleError(
                "This client entry '{0}' cannot be set".format(client_entry_name))

        message_bytes = self._make_message_bytes(
            client_entry, AccessType.SET, args)

        self._com.send_message(message_bytes)

    def get(self, client_name: str, client_entry_name: str, time_out=0.1):
        self.get_async(client_name, client_entry_name)

        max_time = time.time() + time_out
        while not self.is_fresh(client_name, client_entry_name):
            self.update_replies()

            if time.time() > max_time:
                return None

        reply = self.get_reply(client_name, client_entry_name)
        return reply

    def get_all(self, client_name: str, time_out=0.1):
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        replies = {}
        for client_entry_name in client.client_entries.keys():
            reply = self.get(client_name, client_entry_name, time_out)
            replies[client_entry_name] = reply

        return replies

    def save(self, client_name: str, client_entry_name: str):
        self._client_and_client_entry_exists(client_name, client_entry_name)

        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(
            client_entry, AccessType.SAVE, [])

        self._com.send_message(message_bytes)

    def save_all(self, client_name: str):
        self._client_exists(client_name)
        client = self._client_dict[client_name]

        for client_entry_name in client.client_entries.keys():
            self.save(client_name, client_entry_name)

    def get_async(self, client_name: str, client_entry_name: str):
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        client_entry = client.client_entries[client_entry_name]

        message_bytes = self._make_message_bytes(
            client_entry, AccessType.GET, [])

        self._com.send_message(message_bytes)

    def update_replies(self):
        self._com.read_bytes()

        while self._com.bytes_left_in_queue:
            new_message = self._com.extract_message()
            if new_message != None:
                for client in self._client_dict.values():
                    client.read_message(new_message)

            self._com.read_bytes()

    def is_fresh(self, client_name: str, client_entry_name: str):
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]
        return client.is_fresh(client_entry_name)

    def get_reply(self, client_name: str, client_entry_name: str):
        self._client_and_client_entry_exists(client_name, client_entry_name)
        client = self._client_dict[client_name]

        return client.get_reply(client_entry_name)

    def list_clients(self):
        print("\nClients available from '{0}':\n".format(
            self._MODULE_FILE_NAME))

        for client_name in self._client_dict.keys():
            print("\t{0}".format(client_name))

        return

    def list_client_entries(self, client_name: str):
        self._client_exists(client_name)

        # TODO: Make a pretty table with indication of all values
        print("\nEntries available loaded from '{0}': \n".format(client_name))

        client = self._client_dict[client_name]
        for client_entry in client.client_entries.values():
            print(client_entry.data)

        return

    def _client_and_client_entry_exists(self, client_name: str, client_entry_name: str):
        self._client_exists(client_name)

        client = self._client_dict[client_name]

        if client_entry_name not in client.client_entries.keys():
            raise IqModuleError(
                "{0} does not support this client entry: {1}\n".format(client_name, client_entry_name))

        return 1

    def _client_exists(self, client_name: str):
        if client_name not in self._client_dict.keys():
            raise IqModuleError(
                "This module does not support this client: {0}\n".format(client_name))
        return True

    def _make_message_bytes(self, client_entry, access_type: AccessType, args):
        message_maker = DictionaryMessageMaker(
            client_entry, self._module_idn, access_type, args)

        message = ClientWithEntriesMessage(message_maker)

        return message.make_bytes()
