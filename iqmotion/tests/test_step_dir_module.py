import pytest

from iqmotion.iq_devices.step_dir_module import StepDirModule
from iqmotion.tests.helpers import MockCommunicator


class TestStepDirModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        StepDirModule(mock_communicator)
