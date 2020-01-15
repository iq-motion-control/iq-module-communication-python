import pytest

from iqmotion.communication.packet_queue import PacketQueue
from iqmotion.communication.crc import Crc
from iqmotion.communication.custom_error import PacketError


class TestPacketQueue():

    def test__str__(self):
        data = [1, 2, 3]

        pq = PacketQueue()
        pq.put_bytes(data)

        assert data.__str__() == pq.__str__()

    def test_put_bytes_single(self):
        data = 1

        pq = PacketQueue()

        pq.put_bytes(data)

        assert pq._byte_queue[0] == data

    def test_put_bytes_multiple(self):
        data = [1, 2, 3, 4]
        num_bytes = len(data)

        pq = PacketQueue()
        pq.put_bytes(data)

        assert pq._byte_queue[:num_bytes] == data

    def test_put_bytes_array_overflow(self):
        data = [i for i in range(100)]

        with pytest.raises(PacketError) as err:
            pq = PacketQueue()
            pq.put_bytes(data)
            assert pq.put_bytes(1)

        err_str = err.value.message
        assert "PACKET ERROR: Byte Queue Overflow\n" == err_str

    def test_put_bytes_single_overflow(self):
        data = [i for i in range(64)]

        with pytest.raises(PacketError) as err:
            pq = PacketQueue()
            pq.put_bytes(data)
            assert pq.put_bytes(1)

        err_str = err.value.message
        assert "PACKET ERROR: Byte Queue Overflow\n" == err_str

    def test_peek(self):
        data1 = [11, 12, 13]
        data2 = [1, 2, 3, 4]

        fake_message = make_fake_message(data1)
        fake_message.extend(make_fake_message(data2))

        expected_message1 = [3, 0, 11, 12, 13]
        expected_message2 = [4, 0, 1, 2, 3, 4]

        pq = PacketQueue()

        msg_number = 1
        for x in fake_message:
            pq.put_bytes(x)
            msg = pq.peek()
            if msg:
                if msg_number == 1:
                    assert msg == expected_message1
                else:
                    assert msg == expected_message2
                msg_number += 1
                pq.drop_packet()

    def test_drop_packet(self):
        data1 = [11, 12, 13]
        data2 = [1, 2, 3, 4]

        fake_message = make_fake_message(data1)
        fake_message.extend(make_fake_message(data2))

        pq = PacketQueue()
        pq.put_bytes(fake_message)

        assert pq.drop_packet() == False

        # Peek and drop first message
        pq.peek()
        assert pq.drop_packet() == True
        assert pq.drop_packet() == False

        # Peek and drop second messge
        pq.peek()
        assert pq.drop_packet() == True
        assert pq.drop_packet() == False


def make_fake_message(data):
    data_type = 0
    data_len = len(data)

    start = 0x55

    crc_data = [data_len, data_type]
    crc_data.extend(data)
    crc = Crc.make_crc(crc_data)
    crcl = crc & 0xff
    crch = crc >> 8

    fake_message = [start, data_len, data_type]
    fake_message.extend(data)
    fake_message.append(crcl)
    fake_message.append(crch)

    # print(fake_message)

    return bytearray(fake_message)
