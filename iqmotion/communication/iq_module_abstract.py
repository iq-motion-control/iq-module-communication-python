from abc import ABC, abstractmethod

from iqmotion.communication.client import Client

import json
import os


class IqModuleAbstract():
    _clients_dict = {}

    def __init__(self, module_file_name: str):
        self._file_path = os.path.join(
            os.path.dirname(__file__), ('modules/' + module_file_name))

        with open(self._file_path) as json_file:
            module_file = json.load(json_file)

        self._populate_clients(module_file)

    def _populate_clients(self, module_file):
        for client_name in module_file["clients"]:
            self._clients_dict[client_name] = Client(client_name)

    @abstractmethod
    def set(self, client: str, client_entry: str, *args):
        """ this property is too abstract to understand. """

    @abstractmethod
    def get(self, client: str, client_entry: str):
        """ this property is too abstract to understand. """

    @abstractmethod
    def save(self, client: str, client_entry: str):
        """ this property is too abstract to understand. """
