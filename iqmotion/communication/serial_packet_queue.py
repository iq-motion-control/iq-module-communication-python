from iqmotion.communication.packet_queue import PacketQueue
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.packet_parser import PacketParser
from iqmotion.communication.serial_packet_states import SerialStartState
from iqmotion.communication.custom_error import PacketError


class SerialPacketQueue(PacketQueue):
    """ PacketQueue enables extraction of well formed, crc-verified packets from its circular byte queue

    It is a specialized circular queue which takes in raw bytes and returns packet data.
    The returned packet data is a byte array consisting of a type byte followed by data bytes.

    General Packet Format:
        | 0x55 | length | type | ---payload--- | crcL | crcH |
        'length' is the (uint8) number of bytes in 'data'
        'type' is the (uint8) message type
        'payload' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'data', Little-Endian
    """

    _MAX_BYTE_QUEUE_SIZE = 64

    def __init__(self):
        self._byte_queue = CircularQueue(maxlen=self._MAX_BYTE_QUEUE_SIZE)
        self._has_a_packet = 0

    def __str__(self):
        return self._byte_queue.__str__()

    def __len__(self):
        return len(self._byte_queue)

    @property
    def is_empty(self):
        return self._byte_queue.is_empty()

    def put_bytes(self, new_bytes):
        if type(new_bytes) == int:
            if not self._byte_queue.append(new_bytes):
                raise PacketError("Byte Queue Overflow")
        else:
            if not self._byte_queue.extend(new_bytes):
                raise PacketError("Byte Queue Overflow")

    def peek(self):
        if not self._byte_queue.is_empty():
            return self._parse_bytes()
        else:
            raise PacketError("Serial packet queue is empty")

    def _parse_bytes(self):
        packet_state = SerialStartState(self._byte_queue)

        packet_parser = PacketParser(packet_state)
        packet_parser.parse()

        if packet_parser.succesful:
            self._has_a_packet = 1
            return packet_parser.message
        else:
            self._has_a_packet = 0
            return None

    def drop_packet(self):
        if self._has_a_packet:
            msg_len = self._byte_queue[1]

            # + start byte, len, type, crch, crcl
            packet_len = msg_len + 5

            for _ in range(packet_len):
                self._byte_queue.popleft()

            self._has_a_packet = 0
            return 1

        return 0
