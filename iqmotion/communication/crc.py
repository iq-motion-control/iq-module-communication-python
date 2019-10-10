import numpy as np


class Crc():

    @staticmethod
    def MakeCrc(data):
        crc = np.uint16(0xffff)

        for i in range(len(data)):
            crc = Crc.ByteUpdateCrc(crc, data[i])
        pass

        return crc

    @staticmethod
    def ByteUpdateCrc(crc, data: bytes):
        x = np.uint16((crc >> 8) ^ data)
        x ^= np.uint16(x >> 4)

        crc = np.uint16((crc << 8) ^ (x << 12) ^ (x << 5) ^ x)
        return crc

    @staticmethod
    def ArrayUpdateCrc(crc, data, count):
        # Not Handled right now
        pass
