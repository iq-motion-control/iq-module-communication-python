from iqmotion.communication.crc import Crc
# from iqmotion.communication.serial_packet_queue import SerialPacketQueue

import iqmotion as iq

import random
import time


# def Rand(start, end, num):
#     res = []

#     for j in range(num):
#         res.append(random.randint(start, end))

#     return res


def MakeFakePacket(data):
    data_type = 0
    data_len = len(data)

    start = 0x55

    crc_data = [data_len, data_type]
    crc_data.extend(data)
    crc = Crc.make_crc(crc_data)
    crcl = crc & 0xff
    crch = crc >> 8

    packet = [start, data_len, data_type]
    packet.extend(data)
    packet.append(crcl)
    packet.append(crch)

    # print(fake_message)

    return bytearray(packet)


def print_hex(array_of_bytes):
    if array_of_bytes == None:
        print("NONE")
        return

    res = ' '.join(format(x, '02x') for x in array_of_bytes)
    print(res)


if __name__ == "__main__":
    print("\n\n")
    # packet1 = MakeFakePacket([1, 2, 3, 4])
    # packet2 = MakeFakePacket([99, 98, 97, 96])

    # packet_queue = SerialPacketQueue()

    # packet_queue.put_bytes(packet1)
    # packet_queue.put_bytes(packet2)

    # my_packet_1 = packet_queue.peek()
    # packet_queue.drop_packet()
    # print_hex(my_packet_1)

    # my_packet_1 = packet_queue.peek()
    # print_hex(my_packet_1)
    # packet_queue.drop_packet()

    # if not packet_queue.is_empty:
    #     my_packet_1 = packet_queue.peek()
    #     print_hex(my_packet_1)

    # com = iq.Communication
    com = iq.SerialCommunicator('/dev/ttyUSB0')
    module = iq.SpeedModule(com, 0)
    # module.list_clients()
    # module.list_client_entries("brushless_drive")
    # module.list_client_entries("multi_turn_angle_control")
    # module.list_client_entries("propeller_motor_control")
    # module.list_client_entries("gaga")

    # string = "sd2+" + [f]
    # module.set("brushless_drive", "drive_spin_volts", 0)
    # module.set("multi_turn_angle_control", "ctrl_velocity", 1)

    module.get_async("brushless_drive", "obs_angle")
    # ii = 0
    while not module.is_fresh("brushless_drive", "obs_angle"):
        #     ii += 1
        #     print(ii)
        module.update_replies()
    reply = module.get_reply("brushless_drive", "obs_angle")
    print(reply)

    reply2 = module.get("brushless_drive", "obs_angle")
    print(reply2)

    replies = module.get_all("brushless_drive")
    replies = module.get_all("brushless_drive")
    replies = module.get_all("brushless_drive")
    print(replies)

    print("\n\nDONE")
