from iqmotion.communication.communication import Communication
from iqmotion.communication.crc import Crc
from iqmotion.communication.custom_error import CommunicationError
from iqmotion.communication.serial_packet_queue import SerialPacketQueue

import sys
import serial
import glob
from queue import Queue


class SerialCommunication(Communication):

    def __init__(self, port_name: str, baudrate=115200):
        self._ser_handle = self._init_serial(port_name, baudrate)
        self._out_queue = Queue()
        self._in_queue = SerialPacketQueue()

    def __del__(self):
        if self._ser_handle.is_open:
            self._ser_handle.close()
            del self._ser_handle

    def _init_serial(self, port_name: str, baudrate):
        available_ports = self._find_serial_port()

        if port_name not in available_ports:
            pretty_available_ports_str = '\n'.join(
                '\t"{}"'.format(port)for port in available_ports)
            raise CommunicationError(
                "Serial port is not available, here is a list of available ports:\n" + pretty_available_ports_str)

        ser_handle = serial.Serial(port_name, baudrate)

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

    def send_message(self, message: bytearray):
        packet = self._make_packet(message)
        self.add_to_send_queue(packet)
        self.send_now()

    def _make_packet(self, message: bytearray):
        message_length = len(message) - 1  # minus the typeidn
        packet = message.copy()
        packet.insert(0, message_length)
        crc = Crc.make_crc(packet)
        packet.extend(crc)
        packet.insert(0, 0x55)

        return packet

    def add_to_send_queue(self, bytes: bytearray):
        self._out_queue.put(bytes)

    def send_now(self):
        all_messages = bytearray([])
        while not self._out_queue.empty():
            message = self._out_queue.get()
            all_messages.extend(message)

        self._ser_handle.write(all_messages)

    def read_bytes(self):
        bytes_ready = self._ser_handle.in_waiting

        if bytes_ready != 0:
            bytes_read = self._ser_handle.read(bytes_ready)
            self._in_queue.put_bytes(bytes_read)

    @property
    def bytes_left_in_queue(self):
        if self._in_queue.is_empty:
            return False

        return True

    def extract_message(self):
        message = self._in_queue.peek()
        if message != None:
            self._in_queue.drop_packet()

        return message
