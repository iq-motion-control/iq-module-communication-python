from dataclasses import dataclass
import enum
import struct

from iqmotion.client_entries.client_entry import ClientEntry
from iqmotion.client_entries.client_entry_data import ClientEntryData


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
        return "{0:10} | {1:2}: {2:32} {3:4} {4}".format(
            self.type_idn, self.param_idn, self.name, self.format, self.unit
        )


class DictionaryClientEntry(ClientEntry):
    """ DictionaryClientEntry is an implementation of ClientEntry.

        A DictrionaryClientEntry follows this structure:
            {"type_idn":59, "param":"ctrl_angle",
                "param_idn":  3, "format":"f", "unit": "rad" }
    """

    def __init__(self, client_entry_data_dict: dict):
        self._fresh = 0
        self._value = None
        self._data = DictionaryClientEntryData(client_entry_data_dict)

    def read_message(self, msg):
        """ Takes in a message, parses it and save the payload as its value

        General Message Format:
            | type_idn | param_idn | obj/access | value |
            'type_idn' is the (uint8) type identifier
            'param_idn' is the (uint8) param identifier
            'obj/access' high 6 bits are the object identifier, low 2 bits are access direction:
            'value' is the (format) value of the message
        """
        msg_type_idn = msg[0]
        msg_param_idn = msg[1]
        msg_access_type = msg[2] & 3
        msg_value = msg[3:]

        if (msg_type_idn == self.data.type_idn) & (
            msg_param_idn == self.data.param_idn
        ):
            if msg_access_type == AccessType.REPLY.value:
                self.value = msg_value

    @property
    def fresh(self):
        """ Checks if the dictionary client entry value is "fresh" and never been read before

        Returns:
            true:  If value is fresh
            false: If value has been read before
        """
        return self._fresh

    @property
    def value(self):
        """ Gets the value of the Client Entry, the type is define by the format in the client entry

        Returns:
            value (format): Type is defined by format
        """
        self._fresh = 0
        return self._value

    @value.setter
    def value(self, value: bytearray):
        """ Sets the value of the Client Entry and formats it to the right type
        """
        # unpack always returns a tuple
        data_format = self._data.format
        formated_value = struct.unpack(data_format, value)
        if len(data_format) < 2:
            formated_value = formated_value[0]
        self._value = formated_value
        self._fresh = 1

    @property
    def data(self):
        return self._data
