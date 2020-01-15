from iqmotion.communication.client_entry import ClientEntry
from iqmotion.communication.client_entry_data import ClientEntryData

from dataclasses import dataclass
import enum
import struct


class AccessType(enum.Enum):
    GET = 0
    SET = 1
    SAVE = 2
    REPLY = 3


@dataclass
class DictionaryClientEntryData(ClientEntryData):
    type_idn: bytes
    payload_type: bytes
    param_idn: bytes
    format: str
    unit: str
    name: str

    def __init__(self, client_entry_dict: dict):
        self.type_idn = client_entry_dict["type_idn"]
        self.payload_type = 0
        self.param_idn = client_entry_dict["param_idn"]
        self.format = client_entry_dict["format"]
        self.unit = client_entry_dict["unit"]
        self.name = client_entry_dict["param"]

    def __str__(self):
        return "{0:10} | {1:2}: {2:32} {3:4} {4}".format(self.type_idn, self.param_idn, self.name, self.format, self.unit)


class DictionaryClientEntry(ClientEntry):
    def __init__(self, client_entry_data_dict: dict):
        self._fresh = 0
        self._value = None
        self._data = DictionaryClientEntryData(client_entry_data_dict)

    @property
    def fresh(self):
        return self._fresh

    @property
    def value(self):
        self._fresh = 0
        return self._value

    @value.setter
    def value(self, value):
        # unpack always returns a tuple
        format = self._data.format
        formated_value = struct.unpack(format, value)[0]
        self._value = formated_value
        self._fresh = 1

    @property
    def data(self):
        return self._data
