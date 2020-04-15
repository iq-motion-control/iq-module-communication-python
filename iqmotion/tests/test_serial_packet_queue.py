from iqmotion.communication.serial_packet_queue import SerialPacketQueue
from iqmotion.communication.crc import Crc
from iqmotion.custom_errors import PacketQueueError

from iqmotion.tests.helpers import make_fake_packet

import pytest


class TestSerialPacketQueue:
    @pytest.fixture(params=[[1], [1, 2, 3, 4, 5]])
    def serial_packet_queue(self, request):
        if len(request.param) != 1:
            packet = make_fake_packet(request.param)
        else:
            packet = bytes(request.param)

        spq = SerialPacketQueue()
        spq.put_bytes(packet)

        return [spq, packet]

    def test__len__(self, serial_packet_queue):
        spq = serial_packet_queue[0]
        data = serial_packet_queue[1]

        assert len(data) == len(spq)

    def test_is_empty(self, serial_packet_queue):
        spq = serial_packet_queue[0]

        assert False == spq.is_empty

        spq.drop_packet()
        assert True == spq.is_empty

    def test_put_bytes(self):
        data = [i for i in range((255 + 5) * 2)]
        spq = SerialPacketQueue()

        with pytest.raises(PacketQueueError) as err:
            assert spq.put_bytes(data) == 1
            spq.put_bytes(1)

        err_str = err.value.message
        assert "PACKET QUEUE ERROR: Byte Queue Overflow\n" == err_str

        with pytest.raises(PacketQueueError) as err:
            assert spq.put_bytes(data) == 1
            spq.put_bytes([1, 2, 3])

        err_str = err.value.message
        assert "PACKET QUEUE ERROR: Byte Queue Overflow\n" == err_str

    def test_peek(self, serial_packet_queue):
        spq = serial_packet_queue[0]
        data = serial_packet_queue[1]

        if type(data) == bytes:
            assert None == spq.peek()
        else:
            expected_data = data[2:-2]
            assert expected_data == spq.peek()

    def test_peek_empty(self):
        spq = SerialPacketQueue()

        with pytest.raises(PacketQueueError) as err:
            spq.peek()

        err_str = err.value.message
        assert "PACKET QUEUE ERROR: Serial packet queue is empty\n" == err_str

    def test_drop_packet(self, serial_packet_queue):
        spq = serial_packet_queue[0]
        data = serial_packet_queue[1]

        spq.peek()

        if type(data) == bytes:
            assert False == spq.drop_packet()
        else:
            assert True == spq.drop_packet()
