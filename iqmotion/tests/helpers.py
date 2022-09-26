from iqmotion.communication.crc import Crc

# pylint: disable=unused-argument


class MockCommunicator:
    def send_message(self, message: bytearray):
        return

    def add_to_out_queue(self, out_bytes: bytearray):
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


def index_in_list(a_list, index):
    if index < len(a_list):
        return 1

    return 0

class ClientIfDefs:
    brushless_drive = {
        "BRUSHLESS_DRIVE_ANGLE_ADJUST": ["angle_adjust_enable", "motor_emf_calc", "angle_adjustment",
                                         "angle_adjust_max", "angle_adjust_kp", "angle_adjust_ki"],
        "BRUSHLESS_DRIVE_ENABLE_SOFT_CURRENT_LIMIT": ["derate_volts", "motor_i_soft_start", "motor_i_soft_end", "emf",
                                                      "volts_at_mac_amps"],
        "USE_SLEW_LIMIT": ["slew_volts_per_second", "slew_enable"],
        "BRUSHLESS_DRIVE_SUPPLY_CURRENT_LIMIT": ["motoring_supply_current_limit", "regen_supply_current_limit",
                                                 "supply_current_limit_enable"],
        "BRUSHLESS_DRIVE_SUPPLY_CURRENT_LIMIT_CLOSED_LOOP": ["regen_limiting", "regen_limit_adjust",
                                                             "motoring_limiting", "motoring_limit_adjust",
                                                             "regen_limit_kp", "regen_limit_ki", "regen_limit_max",
                                                             "motoring_limit_kp", "motoring_limit_ki",
                                                             "motoring_limit_max"]

    }