from iqmotion.communication.custom_error import PacketError
from iqmotion.communication.payload_maker_abstract import PayloadMakerAbstract
from iqmotion.communication.payload_maker_abstract import PayloadData

import numpy as np
import enum
from dataclasses import dataclass


class AccessType(enum.Enum):
    GET = 0
    SET = 1
    SAVE = 2
    REPLY = 3


@dataclass
class ClientEntryPayloadData(PayloadData):
    param_idn: int
    module_idn: int
    access_type: AccessType
    format: str
    values: any


class ClientEntryPayloadMaker(PayloadMakerAbstract):
    """
    General Payload Format:
        | param_idn | module_idn | access_type | --values-- |
        'param_idn' is the (uint8) client entry idn
        'object_idn' is the (uint8) module idn
        'access_type' is the (uint8) AccessType for the payload
        'values' is a series of (uint8) bytes, serialized Little-Endian
    """

    _value_types = {'': None,
                    'B': np.uint8,
                    'b': np.int8,
                    'f': np.float32,
                    'H': np.uint16,
                    'h': np.int16,
                    'I': np.uint32,
                    'i': np.int32}

    def __init__(self):
        pass

    def make_payload(self, payload_values: PayloadData):
        param_idn = payload_values.param_idn
        module_idn = payload_values.module_idn
        access_type = payload_values.access_type
        format = payload_values.format
        values = payload_values.values

        packet_payload = self._bundle_payload(param_idn,
                                              module_idn,
                                              access_type,
                                              format,
                                              values)

        return packet_payload

    def _bundle_payload(self, param_idn, module_idn, access_type, format, values):
        access = access_type.value + (module_idn*4)
        bundled_payload = bytearray([param_idn, access])

        format_list = list(format)
        values_bytes = bytearray(self._format_values(format_list, values))

        bundled_payload.extend(values_bytes)

        return bundled_payload

    def _format_values(self, format_list, values):
        if isinstance(values, list):
            return self._format_values_list(format_list, values)
        else:
            return self._format_single_value(format_list[0], values)

    def _format_values_list(self, format_list, values_list):
        values_bytes_array = []
        for i, values in enumerate(values_list):
            format = self._parse_format_list(format_list, i)

            formated_values = self._value_types[format](values)
            values_bytes = formated_values.tobytes()

            values_bytes_array.append(values_bytes)

        return values_bytes_array

    def _parse_format_list(self, format_list, current_index):
        if current_index >= len(format_list)-1:
            if format_list[-1] != '*':
                raise PacketError('values too long for client entry')
            else:
                format = format_list[-2]
        else:
            format = format_list[current_index]

        return format

    def _format_single_value(self, format, value):
        formated_value = self._value_types[format](value)
        value_byte = formated_value.tobytes()

        return value_byte
