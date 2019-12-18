from iqmotion.communication.client_entry_abstract import ClientEntryAbstract
from iqmotion.communication.client_entry_abstract import ClientEntryValues


from typing import Union


class ClientEntry(ClientEntryAbstract):
    def __init__(self, client_entry_dict: dict):
        super(ClientEntry, self).__init__(client_entry_dict)

    def get(self):
        pass

    def set(self, args=None):
        if not isinstance(args, (type(None), list, int, tuple)):
            raise TypeError

        print("fake setting:", self._values.name)
        if args == None:
            print("NO VALUES")
        else:
            print(args)

    def save(self, value):
        pass

    def list(self):
        return self._values.__str__()
