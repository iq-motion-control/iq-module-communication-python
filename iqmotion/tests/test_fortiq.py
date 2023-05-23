import pytest

from iqmotion.iq_devices.fortiq_module import Fortiq
from iqmotion.tests.helpers import MockCommunicator
from iqmotion.custom_errors import IqModuleError


class TestFortiqModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_speed_module(self, mock_communicator):
        Fortiq(mock_communicator, firmware="speed")

    def test_stepdir_module(self, mock_communicator):
        Fortiq(mock_communicator, firmware="stepdir")
        Fortiq(mock_communicator, firmware="fortiq_stepdir")

    def test_fortiq_module(self, mock_communicator):
        Fortiq(mock_communicator, firmware="fortiq")

    def test_servo_module(self, mock_communicator):
        Fortiq(mock_communicator, firmware="servo")

    def test_false_module(self, mock_communicator):
        with pytest.raises(IqModuleError):
            Fortiq(mock_communicator, firmware="pulse")