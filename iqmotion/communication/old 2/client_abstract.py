
from abc import ABC, abstractmethod
import json
import os


class ClientAbstract():

    def __init__(self, client_json):

        self._client_json = client_json + ".json"
        self._file_path = os.path.join(
            os.path.dirname(__file__), ('clients/' + self._client_json))

        with open(self._file_path) as json_file:
            client_file = json.load(json_file)

        self.populate_client_entries(client_file)

        self._type_idn = client_file[0]["type_idn"]

    @abstractmethod
    def make_packet(self):
        """ this property is too abstract to understand. """
        return

    @abstractmethod
    def populate_client_entries(self, client_file):
        """ this property is too abstract to understand. """
        return
