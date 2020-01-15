from dataclasses import dataclass


@dataclass
class ClientEntryData():
    type_idn: bytes
    param_idn: bytes
