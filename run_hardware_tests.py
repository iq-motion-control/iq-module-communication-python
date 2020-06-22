import argparse
import sys

import pytest


def speed_test(hardware_type, usb_handle):
    param = [
        "./iqmotion/hardware_tests/test_generic.py",
        "./iqmotion/hardware_tests/test_speed.py",
    ]
    param.append("--usb_handle={}".format(usb_handle))
    param.append("--hardware_type={}".format(hardware_type))
    pytest.main(param)


def servo_test(hardware_type, usb_handle):
    param = [
        "./iqmotion/hardware_tests/test_generic.py",
        "./iqmotion/hardware_tests/test_servo.py",
        "-s",
    ]
    param.append("--usb_handle={}".format(usb_handle))
    param.append("--hardware_type={}".format(hardware_type))
    pytest.main(param)


def step_dir_test(hardware_type, usb_handle):
    param = [
        "./iqmotion/hardware_tests/test_generic.py",
        "./iqmotion/hardware_tests/test_step_dir.py",
    ]
    param.append("--usb_handle={}".format(usb_handle))
    param.append("--hardware_type={}".format(hardware_type))
    pytest.main(param)


def main(hardware_type, usb_handle):
    test_types = {
        "speed": speed_test,
        "servo": servo_test,
        "step_dir": step_dir_test,
    }

    if hardware_type not in test_types.keys():
        print("THIS TYPE IS NOT HANDLED HARDWARE TEST")
        sys.exit()

    test_types[hardware_type](hardware_type, usb_handle)


if __name__ == "__main__":
    handled_hardware_types = ["speed", "servo", "step_dir"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "hardware_type",
        help="Hardware used to run the test",
        choices=handled_hardware_types,
    )
    parser.add_argument(
        "--usb_handle",
        help="Usb handle, defaults to /dev/ttyUSB0",
        default="/dev/ttyUSB0",
    )
    args = parser.parse_args()

    main(args.hardware_type, args.usb_handle)
