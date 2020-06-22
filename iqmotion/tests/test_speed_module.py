import pytest

from iqmotion.iq_devices.speed_module import SpeedModule
from iqmotion.tests.helpers import MockCommunicator


class TestSpeedModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        SpeedModule(mock_communicator)
