from iqmotion.communication.client_entry_abstract import ClientEntryAbstract
from iqmotion.communication.client_entry_abstract import ClientEntryValues


class ClientEntry(ClientEntryAbstract):
    def __init__(self, client_entry_values: ClientEntryValues):
        self._values = client_entry_values

        return
