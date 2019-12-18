from iqmotion.communication.crc import Crc

import iqmotion as iq

import random


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
    crc = Crc.make_crc(crc_data)
    crcl = crc & 0xff
    crch = crc >> 8

    fake_message = [start, data_len, data_type]
    fake_message.extend(data)
    fake_message.append(crcl)
    fake_message.append(crch)

    # print(fake_message)

    return bytearray(fake_message)


if __name__ == "__main__":
    module = iq.IqSpeedModule()
    module.list("brushless_drive")
    # string = "sd2+" + [f]
    module.set("brushless_drive", "drive_mode")
