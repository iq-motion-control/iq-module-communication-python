from iqmotion.communication.communication_interface import CommunicationInterface
from iqmotion.communication.custom_error import CommunicationError
from iqmotion.communication.packet_queue import PacketQueue

import sys
import serial
import glob


class SerialCommunication():
    _ser_handle = serial.Serial()

    def __init__(self, port_name, baudrate=115200):
        try:
            pass
            # self._ser_handle = self._InitializeSerial(port_name, baudrate)
            # self._paquet_queue = PacketQueue()

        except CommunicationError as e:
            print(e.message)
            exit(1)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            exit(1)

    def __del__(self):
        if self._ser_handle.is_open:
            self._ser_handle.close()
            del self._ser_handle

    def Flush(self):
        # am i really usefull ?
        pass

    def GetBytes(self):
        bytes_available = self._ser_handle.in_waiting()

        if not bytes_available:
            return

        input_buffer = self._ser_handle.read(bytes_available)
        self._paquet_queue.PutBytes(input_buffer)

    def PeekPacket(self):
        return self._paquet_queue.Peek()
        # msg_type = []
        # pkt = []

        # buf = self._input_buffer

        # if buf:
        #     if len(buf) <= 100:
        #         buffer = buf
        #         self._input_buffer = bytearray()
        #     else:
        #         buffer = buf[:100]
        #         self._input_buffer = buf[100:-1]
        # else:
        #     buffer = bytearray()

        # self._paquet_queue.PutBytes(buffer)
        # pkt_data = self._paquet_queue.Peek()

        # if not pkt_data:
        #     return

        # msg_type = pkt_data[0]
        # pkt = pkt_data[1:-1]

        # return msg_type, pkt

    def DropPacket(self):
        return self._paquet_queue.DropPacket()

    def SendPacket(self, pkt):
        pass

    def SendMsg(self, msg_spec, msg):
        pass

    # def UnpackMsg(self, msg_spec, pkt_data):
        # pass

    def _InitializeSerial(self, port, baudrate):
        available_ports = self._FindSerialPorts()

        if port not in available_ports:
            pretty_available_ports_str = '\n'.join(
                '\t"{}"'.format(port)for port in available_ports)
            raise CommunicationError(
                "Serial port is not available, here is a list of available ports:\n" + pretty_available_ports_str)

        ser_handle = serial.Serial(port, baudrate)

        return ser_handle

    def _FindSerialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
