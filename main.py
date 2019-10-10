# from iqmotion.communication.world import World
# from iqmotion.communication.clients.client import Client

import iqmotion.communication as iq
# from iqmotion.communication.clients.brushless_drive_client import \
# BrushlessDriveClient
from iqmotion.communication.crc import Crc
from iqmotion.communication.packet_queue import PacketQueue

import random
import copy


def Rand(start, end, num):
    res = []

    for j in range(num):
        res.append(random.randint(start, end))

    return res


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


if __name__ == "__main__":

    com = iq.SerialCommunication("fake")
    mot = iq.BrushlessDriveClient(com)
    mot.get("drive_mode")

    # pq = PacketQueue()

    # data1 = [11, 12, 13]
    # data2 = [5, 4, 3, 2, 1]
    # data3 = [1, 2, 3, 4]
    # fake_message1 = MakeFakeMessage(data1)
    # # # fake_message2 = MakeFakeMessage(data2)
    # fake_message3 = MakeFakeMessage(data3)
    # fake_message1.extend(fake_message3)

    # # pq.PutBytes(bytearray(data2))
    # # pq.PutBytes(bytearray([85, 3]))
    # # pq.PutBytes(fake_message1)
    # pq.PutBytes(fake_message3)
    # print(pq)
    # print(fake_message1)
    # print("-----------------")

    # for x in fake_message1:
    #     print(x)
    #     pq.PutBytes(x)
    #     msg = pq.Peek()
    #     if msg:
    #         print(pq)
    #         print("FULL MESSAGE =", msg)
    #         pq.DropPacket()
    #         print(pq)

    # # while pq.Peek():
    # #     print(pq)
    # #     print("FULL MESSAGE =", pq.Peek())
    # #     pq.DropPacket()
    # # pq.PutBytes(fake_message3[:5])
    # # print(pq)
    # # print(pq.PeekPacket())
    # # pq.PutBytes(fake_message3[5:])
    # # print(pq)
    # # print(pq.PeekPacket())
    # # pq._ParseBytes()
    # # pq._ParseBytes()

    # print("-----------------")
    # print(pq)
