import pytest

from iqmotion.communication.crc import Crc


class TestCrc:
    def test_make_crc(self):
        expected_crc = [61905, 3708, 44461]
        data = [1, 2, 3]
        count = 3
        crcs = []
        for i in range(count):
            crcs.append(Crc.make_crc(data[: i + 1]))

        for i in range(count):
            assert crcs[i] == expected_crc[i]

    def test_updateCrc(self):
        crc = 0xFFFF
        expected_crc = [61905, 49586, 53651]
        data = [1, 2, 3]
        crcs = []

        for i in range(len(data)):
            crcs.append(Crc.byte_update_crc(crc, data[i]))

        for i in range(len(data)):
            assert crcs[i] == expected_crc[i]
