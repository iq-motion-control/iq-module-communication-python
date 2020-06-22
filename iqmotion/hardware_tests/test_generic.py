import time
import sys
import pytest

import iqmotion as iq


class TestGeneric:
    @pytest.fixture
    def iq_module(self, hardware_type, usb_handle):
        hardware_types = {
            "speed": iq.SpeedModule,
            "servo": iq.ServoModule,
            "step_dir": iq.StepDirModule,
        }

        if hardware_type not in hardware_types.keys():
            print("THIS TYPE IS NOT HANDLED IN TEST GENERING")
            sys.exit()

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
                assert value is not None

    def test_get_overload(self, iq_module):
        for _ in range(50):
            result = iq_module.get("system_control", "uid1")
            assert result is not None

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

    def test_set_verify(self, iq_module):
        orginal_kv = iq_module.get("brushless_drive", "motor_Kv")

        success = iq_module.set_verify("brushless_drive", "motor_Kv", orginal_kv + 1)
        assert success

        iq_module.set_verify("brushless_drive", "motor_Kv", orginal_kv, save=True)

    def test_coast(self, iq_module):
        iq_module.set("brushless_drive", "drive_volts", 1)
        time.sleep(0.5)
        drive_mode = iq_module.get_retry("brushless_drive", "drive_mode")

        assert drive_mode != 5

        iq_module.set("brushless_drive", "drive_coast")
        drive_mode = iq_module.get_retry("brushless_drive", "drive_mode")
        assert drive_mode == 5
