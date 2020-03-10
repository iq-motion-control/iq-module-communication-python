from iqmotion.communication.crc import Crc


class MockCommunicator:
    def send_message(self, message: bytearray):
        return

    def add_to_out_queue(self, bytes: bytearray):
        return

    def send_now(self):
        return

    def read_bytes(self):
        return

    def flush_input_buffer(self):
        return

    @property
    def bytes_left_in_queue(self):
        return 0

    def extract_message(self):
        return


class DummySerial:
    def __init__(self, port, baudrate):
        self._port = port
        self._baudrate = baudrate
        self._is_open = True
        self._in_waiting = 0

    def write(self, input_data):
        return

    def read(self, num_bytes):
        return

    def close(self):
        return

    def reset_input_buffer(self):
        return

    @property
    def in_waiting(self):
        return self._in_waiting

    @property
    def is_open(self):
        return self._is_open


def make_fake_packet(data, type_idn=0):
    data_type = type_idn
    data_len = len(data)

    start = 0x55

    crc_data = [data_len, data_type]
    crc_data.extend(data)
    crc = Crc.make_crc(crc_data)
    crcl = crc & 0xFF
    crch = crc >> 8

    packet = [start, data_len, data_type]
    packet.extend(data)
    packet.append(crcl)
    packet.append(crch)

    return bytearray(packet)


def make_fake_message(data, type_idn=0):
    data_type = type_idn
    message = bytearray([data_type])
    message.extend(data)

    return message
