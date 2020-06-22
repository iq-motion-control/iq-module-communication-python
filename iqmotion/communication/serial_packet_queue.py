from iqmotion.communication.packet_queue import PacketQueue
from iqmotion.communication.circular_queue import CircularQueue
from iqmotion.communication.packet_parser import PacketParser
from iqmotion.communication.serial_packet_states import SerialStartState
from iqmotion.custom_errors import PacketQueueError


class SerialPacketQueue(PacketQueue):
    """ SerialPacketQueue enables extraction of well formed, crc-verified packets from its circular byte queue

    It is a specialized circular queue which takes in raw bytes and returns the packet's message.
    The packet's message is a byte array consisting of a type byte followed by payload bytes.

    General Packet Format:
        | 0x55 | length | type | ---payload--- | crcL | crcH |
        'length' is the (uint8) number of bytes in 'data'
        'type' is the (uint8) message type
        'payload' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'data', Little-Endian
    """

    # Don't forget to change the __init__ descriptiton
    _MAX_BYTE_QUEUE_SIZE = (255 + 5) * 2  # size of max packet * 2

    def __init__(self):
        """ Create an empty SerialPacketQueue of constant size 512
        """

        self._byte_queue = CircularQueue(maxlen=self._MAX_BYTE_QUEUE_SIZE)
        self._has_a_packet = 0

    def __len__(self):
        return len(self._byte_queue)

    @property
    def is_empty(self):
        """ Check if queue is empty

        Returns:
            true: if the queue is empty
            false: if the queue has some bytes in it
        """
        return self._byte_queue.is_empty

    @property
    def free_space(self):
        current_size = len(self._byte_queue)
        return self._byte_queue.maxlen - current_size

    def put_bytes(self, new_bytes):
        """ Append bytes to the queue

        Args:
            new_bytes: bytes you want to append.

        Returns:
            true: if succesful

        Raise:
            PacketQueueError("Byte Queue Overflow")
        """
        try:
            iter(new_bytes)
        except TypeError:
            # not iterable
            if not self._byte_queue.append(new_bytes):
                raise PacketQueueError("Byte Queue Overflow")
        else:
            # iterable
            if not self._byte_queue.extend(new_bytes):
                raise PacketQueueError("Byte Queue Overflow")

        return 1

    def peek(self):
        """ Peeks for the first available packet in the queue and extract its message

        Returns:
            bytearray: The first available message
            None: There was no well form packet in the queue

        Raise:
        When the queue is empty
            PacketQueueError("Serial packet queue is empty")
        """
        if self._byte_queue.is_empty:
            raise PacketQueueError("Serial packet queue is empty")

        return self._parse_bytes()

    def _parse_bytes(self):
        packet_state = SerialStartState(self._byte_queue)

        packet_parser = PacketParser(packet_state)
        packet_parser.parse()

        if not packet_parser.succesful:
            self._has_a_packet = 0
            return None

        self._has_a_packet = 1
        return packet_parser.message

    def clear(self):
        """ Clears the queue """
        self._byte_queue.clear()

    def drop_packet(self):
        """ Drops the first packet available in the queue

        Returns:
            True: a packet was droped
            False: no packet was droped
        """
        # no need to parse if you know there is a packet
        if self._has_a_packet:
            self._pop_packet_bytes()
            self._has_a_packet = 0
            return True

        self._parse_bytes()
        if self._has_a_packet:
            self._pop_packet_bytes()
            self._has_a_packet = 0
            return True

        return False

    def _pop_packet_bytes(self):
        msg_len = self._byte_queue[1]

        # + start byte, len, type, crch, crcl
        packet_len = msg_len + 5

        for _ in range(packet_len):
            self._byte_queue.popleft()
