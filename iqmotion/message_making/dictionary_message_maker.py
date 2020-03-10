from iqmotion.message_making.message_maker import MessageMaker
from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntry
from iqmotion.client_entries.dictionary_client_entry import AccessType
from iqmotion.client_entries.dictionary_client_entry import DictionaryClientEntryData
from iqmotion.custom_errors import MessageMakerError

from dataclasses import dataclass
import enum
import numpy as np


@dataclass
class DictionaryMessageMakerData:
    type_idn: bytes
    param_idn: bytes
    module_idn: bytes
    access_type: AccessType
    format: str
    value: any

    def __init__(
        self,
        client_entry_data: DictionaryClientEntryData,
        module_idn: bytes,
        access_type: AccessType,
        value,
    ):

        self.type_idn = client_entry_data.type_idn
        self.param_idn = client_entry_data.param_idn
        self.module_idn = module_idn
        self.access_type = access_type
        self.format = client_entry_data.format
        self.values = value


class DictionaryMessageMaker(MessageMaker):
    """ DictionaryMessageMaker is an implementation of MessageMaker
    This class defines how to make a message from a dictionary client entry
    """

    def __init__(
        self,
        client_entry: DictionaryClientEntry,
        module_idn: bytes,
        access_type: AccessType,
        values,
    ):
        """ Returns a DictonaryMessageMaker object to create dictionary client entry messages

        Args:
            client_entry (DictionaryClientEntry): client entry used to make the message
            module_idn (bytes): id of the module
            access_type (AccessType): Access type of the message
            values (int/list): values to be put in the message
        """

        self._data = DictionaryMessageMakerData(
            client_entry.data, module_idn, access_type, values
        )

        self._value_types = {
            "": None,
            "B": np.uint8,
            "b": np.int8,
            "f": np.float32,
            "H": np.uint16,
            "h": np.int16,
            "I": np.uint32,
            "i": np.int32,
        }

    def make(self):
        """ Makes the message

        Returns:
            bytearray: the message made

        Raises:
            MessageMakerError: if values too long for client entry
        """
        message = bytearray([self._data.type_idn])
        payload = self._make_payload()
        message.extend(payload)

        return message

    def _make_payload(self):
        param_idn = self._data.param_idn
        module_idn = self._data.module_idn
        access_type = self._data.access_type
        format = self._data.format
        values = self._data.values

        access = access_type.value + (module_idn * 4)
        payload = bytearray([param_idn, access])
        values_bytes = self._format_values(list(format), values)
        payload.extend(values_bytes)

        return payload

    def _format_values(self, format_list, values):
        if isinstance(values, list):
            formated_values = self._format_values_list(format_list, values)
        elif len(format_list) == 0:
            formated_values = []
        else:
            formated_values = self._format_single_value(format_list[0], values)

        return bytearray(formated_values)

    def _format_values_list(self, format_list, values_list):
        values_bytes_array = bytearray([])
        for i, values in enumerate(values_list):
            format = self._parse_format_list(format_list, i)

            formated_values = self._value_types[format](values)
            values_bytes = formated_values.tobytes()

            values_bytes_array.extend(values_bytes)

        return values_bytes_array

    def _parse_format_list(self, format_list, current_index):
        if current_index >= len(format_list) - 1:
            if format_list[-1] != "*":
                raise MessageMakerError("values too long for client entry")
            else:
                format = format_list[-2]
        else:
            format = format_list[current_index]

        return format

    def _format_single_value(self, format, value):
        formated_value = self._value_types[format](value)
        value_byte = formated_value.tobytes()

        return value_byte
