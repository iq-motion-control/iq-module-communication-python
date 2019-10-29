from abc import ABC, abstractmethod


class IqModuleAbstract():
    _clients_dict = {}

    @abstractmethod
    def populate_clients_map(self):
        pass

    def set(self, client: str, client_entry: str, *args):
        pass

    def get(self, client: str, client_entry: str):
        pass

    def save(self, client: str, client_entry: str):
        pass
