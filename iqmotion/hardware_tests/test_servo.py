import iqmotion as iq

import pytest


class TestStepDir:
    @pytest.fixture
    def iq_module(self, hardware_type, usb_handle):
        hardware_types = {
            "servo": iq.ServoModule,
        }

        if hardware_type not in hardware_types.keys():
            print("THIS TYPE IS NOT HANDLED IN TEST SPEED")
            exit()

        com = iq.SerialCommunicator(usb_handle)
        iq_module = hardware_types[hardware_type](com, 0)

        return iq_module

    def test_ramp_velocity(self, iq_module):
        assert iq_module.ramp_velocity(100, 1)
        assert iq_module.ramp_velocity(-100, 2)
        assert iq_module.ramp_velocity(0, 1)

    def test_ramp_volts(self, iq_module):
        assert iq_module.ramp_volts(2, 1)
        assert iq_module.ramp_volts(-2, 2)
        assert iq_module.ramp_volts(0, 1)

    def test_ramp_volts_slew(self, iq_module):
        assert iq_module.ramp_volts_slew(2, 1)
        assert iq_module.ramp_volts_slew(-2, 1)
        assert iq_module.ramp_volts_slew(0, 1)
