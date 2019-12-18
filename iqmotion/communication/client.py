from iqmotion.communication.client_entry_abstract import ClientEntryValues
from iqmotion.communication.client_entry_abstract import ClientEntryAbstract
from iqmotion.communication.client_entry import ClientEntry
from iqmotion.communication.custom_error import ClientError

import json
import os


class Client:
    _client_entries_dict = {}

    def __init__(self, client_json):
        self._client_json = client_json + ".json"
        self._file_path = os.path.join(
            os.path.dirname(__file__), ('clients/' + self._client_json))

        with open(self._file_path) as json_file:
            client_file = json.load(json_file)

        self._populate_client_entries(client_file)

    def get(self):
        pass

    def set(self, client_entry: str, args=None):
        if client_entry not in self._client_entries_dict.keys():
            raise ClientError("Client_entry not in Client")

        client_entry = self._client_entries_dict[client_entry]
        client_entry.set(args)

        return 1

    def save(self, value):
        pass

    def list(self):
        print("\nParameter set loaded from: {0}".format(self._client_json))

        # TODO: Make a pretty table with indication of all values
        for values in self._client_entries_dict.values():
            print(values.list())
        print("\n")

        return self._client_entries_dict

    def _populate_client_entries(self, client_file):
        for client_entry_dict in client_file:
            client_entry_name = client_entry_dict["param"]
            self._client_entries_dict[client_entry_name] = ClientEntry(
                client_entry_dict)

        return
