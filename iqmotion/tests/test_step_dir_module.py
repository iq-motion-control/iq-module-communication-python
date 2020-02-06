from iqmotion.iq_devices.set_dir_module import StepDirModule
from iqmotion.tests.helpers import MockCommunicator

import pytest


@pytest.fixture
def mock_communicator():
    mock_class = MockCommunicator()
    return mock_class


def test_module(mock_communicator):
    StepDirModule(mock_communicator)
