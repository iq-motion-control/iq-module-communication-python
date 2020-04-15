def pytest_addoption(parser):
    parser.addoption("--hardware_type", action="store", default="speed")
    parser.addoption("--usb_handle", action="store", default="/dev/ttyUSB0")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.hardware_type
    if "hardware_type" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("hardware_type", [option_value])

    option_value = metafunc.config.option.usb_handle
    if "usb_handle" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("usb_handle", [option_value])
