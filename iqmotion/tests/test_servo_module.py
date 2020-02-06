from iqmotion.iq_devices.servo_module import ServoModule
from iqmotion.tests.helpers import MockCommunicator

import pytest


@pytest.fixture
def mock_communicator():
    mock_class = MockCommunicator()
    return mock_class


def test_module(mock_communicator):
    ServoModule(mock_communicator)
