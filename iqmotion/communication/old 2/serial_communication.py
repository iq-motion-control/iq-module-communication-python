from iqmotion.communication.custom_error import CommunicationError
from iqmotion.communication.communication_abstract import CommunicationAbsract

import sys
import serial
import glob


class SerialCommunication():
    """
    General Packet Format:
        | 0x55 | length | type | ---data--- | crcL | crcH |
        'length' is the (uint8) number of bytes in 'data'
        'type' is the (uint8) message type
        'data' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'data', Little-Endian
    """
    _ser_handle = serial.Serial()

    def __init__(self, port_name, baudrate=115200):
        self._ser_handle = self._init_serial(port_name, baudrate)
        # self._paquet_queue = PacketQueue()

    def __del__(self):
        if self._ser_handle.is_open:
            self._ser_handle.close()
            del self._ser_handle

    def send_packet(self, packet_type, packet_data):
        pass
        # self._ser_handle.flush()
        # self._ser_handle.write(packet)

    def _init_serial(self, port, baudrate):
        available_ports = self._find_serial_port()

        if port not in available_ports:
            pretty_available_ports_str = '\n'.join(
                '\t"{}"'.format(port)for port in available_ports)
            raise CommunicationError(
                "Serial port is not available, here is a list of available ports:\n" + pretty_available_ports_str)

        ser_handle = serial.Serial(port, baudrate)

        return ser_handle

    def _find_serial_port(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        working_ports = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                working_ports.append(port)
            except (OSError, serial.SerialException):
                pass

        return working_ports

    # def _get_crc_bytes(self, bundled_values):
    #     crc = Crc.make_crc(bundled_values)
    #     crcl = crc & 0xff
    #     crch = crc >> 8

    #     return crcl, crch

    # def _concatenate_packet_bytes(self, bundled_values, packet_type):
    #     packet_length = len(bundled_values)

    #     packet = bytearray([packet_length, packet_type])
    #     packet.extend(bundled_values)

    #     crcl, crch = self._get_crc_bytes(packet)

    #     packet.insert(0, 0x55)
    #     packet.append(crcl)
    #     packet.append(crch)

    #     return packet
