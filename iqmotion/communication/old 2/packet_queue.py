from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.packet_states import StartState
from iqmotion.communication.custom_error import PacketError


# TODO: write comments
class PacketQueue():
    """ PacketQueue enables extraction of well formed, crc-verified packets from its circular byte queue

    It is a specialized circular queue which takes in raw bytes and returns packet data.
    The returned packet data is a byte array consisting of a type byte followed by data bytes.

    General Packet Format:
        | 0x55 | length | type | ---data--- | crcL | crcH |
        'length' is the (uint8) number of bytes in 'data'
        'type' is the (uint8) message type
        'data' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'data', Little-Endian
    """
    _MAX_BYTE_QUEUE_SIZE = 64

    def __init__(self):
        self._byte_queue = CircularQueue(maxlen=self._MAX_BYTE_QUEUE_SIZE)
        self._has_a_packet = 0
        self._packet_start_index = 0
        self._packet_end_index = 0

    def __str__(self):
        return self._byte_queue.__str__()

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

    def _parse_bytes(self):
        start_index = 0

        packet_state = StartState(self._byte_queue, start_index, 0, 0)
        while not packet_state.is_done:
            packet_state.parse()
            packet_state = packet_state.find_next_state()

        if packet_state.succesful:
            self._has_a_packet = 1
            return packet_state.get_message()
        else:
            self._has_a_packet = 0
            return None

    def drop_packet(self):
        if self._has_a_packet:
            msg_len = self._byte_queue[self._packet_start_index+1]

            # + start byte, len, type, crch, crcl
            packet_len = msg_len + 5

            for _ in range(packet_len):
                self._byte_queue.popleft()

            self._has_a_packet = 0
            return 1

        return 0
