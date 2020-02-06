from dataclasses import dataclass


@dataclass
class ClientEntryData:
    """ ClientEntryData is an interface data class for the different client entry implementations.
    They data available in a client entry should be represented as a ClientEntryData.
    It is the implementaiton's job to also implement this data class and add any needed infromation.
    """

    type_idn: bytes
    param_idn: bytes
