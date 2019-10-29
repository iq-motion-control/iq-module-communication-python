from dataclasses import dataclass


@dataclass
class ClientEntryValues:
    type_idn: bytes
    sub_idn: bytes
    format: str
    unit: str
    name: str


class ClientEntryAbstract:
    _values = ClientEntryValues

    def get(self):
        pass

    def set(self, *args):
        pass

    def save(self, value):
        pass
