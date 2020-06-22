import pytest

from iqmotion.iq_devices.servo_module import ServoModule
from iqmotion.tests.helpers import MockCommunicator


class TestServoModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        ServoModule(mock_communicator)

