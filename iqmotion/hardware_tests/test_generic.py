import iqmotion as iq

import pytest
import time


class TestGeneric:
    @pytest.fixture
    def iq_module(self, hardware_type, usb_handle):
        hardware_types = {
            "speed": iq.SpeedModule,
            "servo": iq.ServoModule,
            "step_dir": iq.StepDirModule,
            "pulsing": iq.PulsingModule,
        }

        if hardware_type not in hardware_types.keys():
            print("THIS TYPE IS NOT HANDLED IN TEST GENERING")
            exit()

        com = iq.SerialCommunicator(usb_handle)
        iq_module = hardware_types[hardware_type](com, 0)

        # timeout for speed modules
        if hardware_type == "speed":
            iq_module.set("propeller_motor_control", "timeout", 10)

        return iq_module

    def test_get_all(self, iq_module):
        empty_entries = ["reboot_program", "reboot_boot_loader"]

        results = iq_module.get_all("system_control")
        for key, value in results.items():
            if key not in empty_entries:
                assert value != None

    def test_get_overload(self, iq_module):
        for _ in range(50):
            result = iq_module.get("system_control", "uid1")
            assert result != None

    def test_get_async_overload(self, iq_module):
        angle_samples = []
        sampling_time = 5

        start_time = time.perf_counter()
        while time.perf_counter() < start_time + sampling_time:
            iq_module.get_async("brushless_drive", "obs_angle")
            all_bytes_read = iq_module.update_replies()
            while not all_bytes_read:
                all_bytes_read = iq_module.update_replies()

            if iq_module.is_fresh("brushless_drive", "obs_angle"):
                current_angle = iq_module.get_reply("brushless_drive", "obs_angle")
                angle_samples.append(current_angle)

        assert None not in angle_samples
