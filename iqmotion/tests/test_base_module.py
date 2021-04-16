import pytest

from iqmotion.iq_devices.base_iq_module import BaseIqModule
from iqmotion.tests.helpers import MockCommunicator


class TestBaseIqModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        BaseIqModule(mock_communicator)
