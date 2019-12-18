

class PacketMaker():
    """
    General Packet Format:
        | 0x55 | length | type | ---data--- | crcL | crcH |
        'length' is the (uint8) number of bytes in 'data'
        'type' is the (uint8) message type
        'data' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'data', Little-Endian
    """

    def __init__(self):
        pass

    def make(self, spec, msg):
        self._BundleMsg(spec, msg)

    def _bundle_msg(self, spec, msg):
        msg_type = spec["Type"]
        spec_fields = spec["Fields"]

        data_list = []
        for field_key, field_value in spec_fields.items():
            data = field_value(msg[field_key])
            data_list.append(data)

    def _bundle_packet(self):
        pass
