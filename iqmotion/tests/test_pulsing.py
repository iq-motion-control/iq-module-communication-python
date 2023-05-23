import pytest

from iqmotion.iq_devices.pulsing_module import PulsingModule
from iqmotion.tests.helpers import MockCommunicator


class TestPulsingModuleModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_pulsing_module(self, mock_communicator):
        PulsingModule(mock_communicator)
