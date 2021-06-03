import pytest
import os

from iqmotion.iq_devices.custom_iq_module import CustomIqModule

from iqmotion.tests.helpers import MockCommunicator


class NewModule(CustomIqModule):
    _DEFAULT_CONTROL_CLIENT = "CONTROL"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "VEL"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "VOLTS"
    _MODULE_FILE_NAME = "new_module.json"

    def __init__(
        self, com, module_idn=0, extra_clients=None,
    ):
        super().__init__(__file__, com, module_idn, extra_clients=extra_clients)

class NonExtraModule(CustomIqModule):
    _DEFAULT_CONTROL_CLIENT = "CONTROL"
    _DEFAULT_VELOCITY_CLIENT_ENTRY = "VEL"
    _DEFAULT_VOLTS_CLIENT_ENTRY = "VOLTS"
    _MODULE_FILE_NAME = "non_extra_module.json"

    def __init__(
        self, com, module_idn=0, extra_clients=None,
    ):
        super().__init__(__file__, com, module_idn, extra_clients=extra_clients)


@pytest.fixture
def mock_communicator():
    mock_class = MockCommunicator()
    return mock_class


# pylint: disable=redefined-outer-name
def test_custom_iq_module(mock_communicator):
    expected_clients = set(
        [
            "brushless_drive",
            "propeller_motor_control",
            "anticogging",
            "buzzer_control",
            "esc_propeller_input_parser",
            "hobby_input",
            "persistent_memory",
            "power_monitor",
            "serial_interface",
            "servo_input_parser",
            "step_direction_input",
            "system_control",
            "temperature_estimator",
            "temperature_monitor_uc",
            "extra_client",
        ],
    )
    iq_module = NewModule(mock_communicator, 0)
    client_dict = set(iq_module._client_dict.keys())
    assert client_dict == expected_clients

def test_extra_clients_iq_module(mock_communicator):
    expected_clients = set(
        [
            "brushless_drive",
            "propeller_motor_control",
            "anticogging",
            "buzzer_control",
            "esc_propeller_input_parser",
            "hobby_input",
            "persistent_memory",
            "power_monitor",
            "serial_interface",
            "servo_input_parser",
            "step_direction_input",
            "system_control",
            "temperature_estimator",
            "temperature_monitor_uc",
            "extra_client",
        ],
    )

    extra_client = os.path.join(os.path.dirname(__file__), ("extra_client_files/extra_client.json"))
    print(extra_client)

    iq_module = NonExtraModule(mock_communicator, 0, extra_clients=[extra_client])
    client_dict = set(iq_module._client_dict.keys())
    assert client_dict == expected_clients