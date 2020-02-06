from iqmotion.iq_devices.speed_module import SpeedModule
from iqmotion.tests.helpers import MockCommunicator

import pytest


@pytest.fixture
def mock_communicator():
    mock_class = MockCommunicator()
    return mock_class


def test_module(mock_communicator):
    SpeedModule(mock_communicator)
