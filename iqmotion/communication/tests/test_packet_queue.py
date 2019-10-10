import pytest

from iqmotion.communication.packet_queue import PacketQueue
from iqmotion.communication.crc import Crc


class TestPacketQueue():

    def test_PutBytes_single(self):
        data = 1

        pq = PacketQueue()

        pq.PutBytes(data)

        assert pq._byte_queue[0] == data

    def test_PutBytes_multiple(self):
        data = [1, 2, 3, 4]
        num_bytes = len(data)

        pq = PacketQueue()

        pq.PutBytes(data)

        assert pq._byte_queue[:num_bytes] == data

    def test_Peek(self):
        data1 = [11, 12, 13]
        data2 = [1, 2, 3, 4]

        fake_message = MakeFakeMessage(data1)
        fake_message.extend(MakeFakeMessage(data2))

        expected_message1 = [3, 0, 11, 12, 13]
        expected_message2 = [4, 0, 1, 2, 3, 4]

        pq = PacketQueue()

        msg_number = 1
        for x in fake_message:
            pq.PutBytes(x)
            msg = pq.Peek()
            if msg:
                if msg_number == 1:
                    assert msg == expected_message1
                else:
                    assert msg == expected_message2
                msg_number += 1
                pq.DropPacket()


def MakeFakeMessage(data):
    data_type = 0
    data_len = len(data)

    start = 0x55

    crc_data = [data_len, data_type]
    crc_data.extend(data)
    crc = Crc.MakeCrc(crc_data)
    crcl = crc & 0xff
    crch = crc >> 8

    fake_message = [start, data_len, data_type]
    fake_message.extend(data)
    fake_message.append(crcl)
    fake_message.append(crch)

    # print(fake_message)

    return bytearray(fake_message)
