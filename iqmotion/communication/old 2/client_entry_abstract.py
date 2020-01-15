from iqmotion.communication.payload_maker_abstract import PayloadMakerAbstract

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ClientEntryValues:
    type_idn: bytes
    param_idn: bytes
    format: str
    unit: str
    name: str
    # msg_type: int

    def __init__(self, client_entry_dict: dict):
        self.type_idn = client_entry_dict["type_idn"]
        self.param_idn = client_entry_dict["param_idn"]
        self.format = client_entry_dict["format"]
        self.unit = client_entry_dict["unit"]
        self.name = client_entry_dict["param"]
        # self.msg_type = client_entry_dict["msg_type"]

    def __str__(self):
        return "{0:10} | {1:2}: {2:32} {3:4} {4}".format(self.type_idn, self.param_idn, self.name, self.format, self.unit)


class ClientEntryAbstract:
    _values = ClientEntryValues

    def __init__(self, module_idn, client_entry_dict: dict, payload_maker: PayloadMakerAbstract):
        self._values = ClientEntryValues(client_entry_dict)
        self._module_idn = module_idn
        self._payload_maker = payload_maker

    @abstractmethod
    def make_get_payload(self):
        """ this property is too abstract to understand. """

    @abstractmethod
    def make_set_payload(self, *args):
        """ this property is too abstract to understand. """

    @abstractmethod
    def make_save_payload(self, value):
        """ this property is too abstract to understand. """

    @abstractmethod
    def list(self):
        """ this property is too abstract to understand. """
