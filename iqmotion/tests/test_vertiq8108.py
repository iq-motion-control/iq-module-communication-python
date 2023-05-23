import pytest

from iqmotion.iq_devices.vertiq8108_module import Vertiq8108
from iqmotion.tests.helpers import MockCommunicator
from iqmotion.custom_errors import IqModuleError


class TestVertiq8108Module:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_speed_module(self, mock_communicator):
        Vertiq8108(mock_communicator, firmware="speed")

    def test_stepdir_module(self, mock_communicator):
        with pytest.raises(IqModuleError):
            Vertiq8108(mock_communicator, firmware="stepdir")

    # def test_servo_module(self, mock_communicator):
    #     Vertiq8108(mock_communicator, firmware="servo")

    def test_false_module(self, mock_communicator):
        with pytest.raises(IqModuleError):
            Vertiq8108(mock_communicator, firmware="pulse")