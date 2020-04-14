from iqmotion.iq_devices.speed_module import SpeedModule
from iqmotion.tests.helpers import MockCommunicator
from iqmotion.iq_devices.ramper import Ramper

import pytest
from unittest.mock import patch, Mock, MagicMock, call, PropertyMock


class TestSpeedModule:
    @pytest.fixture
    def mock_communicator(self):
        mock_class = MockCommunicator()
        return mock_class

    def test_module(self, mock_communicator):
        SpeedModule(mock_communicator)

    def test_ramp_velocity(self, mock_communicator):
        Ramper.ramp_velocity = MagicMock()
        module = SpeedModule(mock_communicator)

        velocity_client = "propeller_motor_control"
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
        module = SpeedModule(mock_communicator)

        volts_client = "propeller_motor_control"
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
        module = SpeedModule(mock_communicator)

        final_volts = 5
        slew_rate = 2

        module.ramp_volts_slew(final_volts, slew_rate)

        Ramper.ramp_volts_slew.assert_called_with(module, final_volts, slew_rate)
        pass
