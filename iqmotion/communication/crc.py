import numpy as np


class Crc:
    """ A static class that creates a (uint16) CRC value from some list of bytes
    """

    @staticmethod
    def make_crc(data):
        """ Make a crc from a list of bytes

        Args:
            data (List): a list of bytes to make the crc from

        Returns:
            crc (np.uint16): a uint16 CRC
        """
        crc = np.uint16(0xFFFF)

        for i, _ in enumerate(data):
            crc = Crc.byte_update_crc(crc, data[i])

        return crc

    @staticmethod
    def byte_update_crc(crc, data: bytes):
        """ Update a current crc with a new byte 

        Args:
            crc (np.uint16): current crc value
            data (bytes): the byte used to update the crc

        Returns:
            crc (np.uint16): new updated crc
        """
        x = np.uint16((crc >> 8) ^ data)
        x ^= np.uint16(x >> 4)

        crc = np.uint16((crc << 8) ^ (x << 12) ^ (x << 5) ^ x)
        return crc
