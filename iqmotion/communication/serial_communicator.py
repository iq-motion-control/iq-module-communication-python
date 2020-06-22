import sys
import glob
from queue import Queue

import serial

from iqmotion.communication.communicator import Communicator
from iqmotion.communication.crc import Crc
from iqmotion.communication.serial_packet_queue import SerialPacketQueue
from iqmotion.custom_errors import CommunicationError


class SerialCommunicator(Communicator):
    """SericalCommunicator enables to create serial packets with a message inside
    as well as extract well formed messages from its serial packets

    General Packet Format:
        | 0x55 | length | message | crcL | crcH |
        'length' is the (uint8) number of bytes in 'payload'
        'message' is a series of (uint8) bytes, serialized Little-Endian
        'crc' is the (uint16) CRC value for 'length'+'type'+'payload', Little-Endian
    """

    def __init__(self, port_name: str, baudrate=115200):
        """ Creates a SericalCommunication with a given port and baudrate

        Args:
            port_name (str): serial port name
            baudrate (int): baudrate for serial communication
        """
        self._ser_handle = self._init_serial(port_name, baudrate)
        self._out_queue = Queue()
        self._in_queue = SerialPacketQueue()

    def __del__(self):
        if hasattr(self, "_ser_handle") and self._ser_handle.is_open:
            self._ser_handle.close()
            del self._ser_handle

    def _init_serial(self, port_name: str, baudrate):
        try:
            ser_handle = serial.Serial(port_name, baudrate)

        except serial.SerialException:
            available_ports = self._find_serial_port()
            pretty_available_ports_str = "\n".join(
                '\t"{}"'.format(port) for port in available_ports
            )
            raise CommunicationError(
                f"Serial port '{port_name}' is not available, here is a list of available ports:\n{pretty_available_ports_str}"
            )

        return ser_handle

    def _find_serial_port(self):
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

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
        """ Packages a message and sends it through serial

        Args:
            message (bytearray): message to be packaged and sent
        """

        packet = self._make_packet(message)
        self.add_to_out_queue(packet)
        self.send_now()

    def _make_packet(self, message: bytearray):
        message_length = len(message) - 1  # minus the typeidn
        packet = message.copy()
        packet.insert(0, message_length)
        crc = Crc.make_crc(packet)
        packet.extend(crc)
        packet.insert(0, 0x55)

        return packet

    def add_to_out_queue(self, out_bytes: bytearray):
        """ Add raw bytes to the out queue, call "send_now" to send

        Args:
            bytes (bytearray): raw bytes to send
        """
        self._out_queue.put(out_bytes)

    def send_now(self):
        """ Sends everything that was added to the out queue
        """
        all_messages = bytearray([])
        while not self._out_queue.empty():
            message = self._out_queue.get()
            all_messages.extend(message)

        self._ser_handle.write(all_messages)

    def flush_input_buffer(self):
        """Flushes all the bytes left in the serial buffer in
        """
        self._in_queue.clear()
        self._ser_handle.reset_input_buffer()

    def read_bytes(self):
        """ Read bytes available in the serial port and puts them inside the packet queue.

        If there are more bytes ready to be read from serial than space in the packet queue, 
        only read up to the max packet queue size
        
        Returns:
            bool -- True if every bytes were read from the serial buffer, False otherwise
        """
        bytes_ready = self._ser_handle.in_waiting
        free_space = self._in_queue.free_space

        if bytes_ready > free_space:
            bytes_read = self._ser_handle.read(free_space)
            every_bytes_read = 0

        else:
            bytes_read = self._ser_handle.read(bytes_ready)
            every_bytes_read = 1

        self._in_queue.put_bytes(bytes_read)

        return every_bytes_read

    @property
    def bytes_left_in_queue(self):
        """ Returns the amount of bytes left in the packet queue
        """
        if self._in_queue.is_empty:
            return False

        return True

    def extract_message(self):
        """ Extract a well form message from the packet queue

        Returns:
            message (bytearray): if parsing successfull
            message (None): if not message is available
        """
        if self.bytes_left_in_queue:
            message = self._in_queue.peek()
            self._in_queue.drop_packet()
        else:
            message = None

        return message
