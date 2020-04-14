from iqmotion.iq_devices.step_dir_module import StepDirModule
from iqmotion.tests.helpers import MockCommunicator
from iqmotion.iq_devices.ramper import Ramper

import pytest
from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestStepDirModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        StepDirModule(mock_communicator)

    def test_ramp_velocity(self, mock_communicator):
        Ramper.ramp_velocity = MagicMock()
        module = StepDirModule(mock_communicator)

        velocity_client = "multi_turn_angle_control"
        velocity_client_entry = "ctrl_velocity"
        final_velocity = 5
        total_time = 2
        time_steps = 10

        module.ramp_velocity(final_velocity, total_time, time_steps=time_steps)

        Ramper.ramp_velocity.assert_called_with(
            module,
            velocity_client,
            velocity_client_entry,
            final_velocity,
            total_time,
            time_steps,
        )

    def test_ramp_volts(self, mock_communicator):
        Ramper.ramp_volts = MagicMock()
        module = StepDirModule(mock_communicator)

        volts_client = "multi_turn_angle_control"
        volts_client_entry = "ctrl_volts"
        final_volts = 5
        total_time = 2
        time_steps = 10

        module.ramp_volts(final_volts, total_time, time_steps=time_steps)

        Ramper.ramp_volts.assert_called_with(
            module,
            volts_client,
            volts_client_entry,
            final_volts,
            total_time,
            time_steps,
        )

    def test_ramp_slew(self, mock_communicator):
        Ramper.ramp_volts_slew = MagicMock()
        module = StepDirModule(mock_communicator)

        final_volts = 5
        slew_rate = 2

        module.ramp_volts_slew(final_volts, slew_rate)

        Ramper.ramp_volts_slew.assert_called_with(module, final_volts, slew_rate)
        pass
