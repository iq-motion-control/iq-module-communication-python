import time

import pytest
import iqmotion as iq
import iqmotion.custom_errors


class TestApiSpeed8108:

    @pytest.fixture
    def com_port(self):
        return iq.SerialCommunicator("COM4")

    @pytest.fixture
    def vertiq_8108(self, com_port):
        return iq.Vertiq8108(com_port, 0)

    @pytest.fixture
    def client_list(self, vertiq_8108):
        return vertiq_8108.return_clients()

    def test_get_all(self, vertiq_8108, client_list):
        assert client_list is not None

        print('\n')
        for client in client_list:
            print(f"\ntesting {client}")
            clients = vertiq_8108.get_all(client)
            assert clients is not None

            for client_entry in clients:
                print(f"{client_entry}: {clients[client_entry]}")

    def test_brushless_drive(self, vertiq_8108, client_list):
        brushless_drive = "brushless_drive"
        assert brushless_drive in client_list

        brushless_drive_entries = vertiq_8108.return_client_entries(brushless_drive)
        assert brushless_drive_entries is not None

        regen_limit_adjust = "regen_limit_adjust"
        print(f"\nConfirming {regen_limit_adjust} is removed from {brushless_drive}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(brushless_drive, regen_limit_adjust)

        motoring_limit_adjust = "motoring_limit_adjust"
        print(f"\nConfirming {motoring_limit_adjust} is removed from {brushless_drive}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(brushless_drive, motoring_limit_adjust)

        scaling_commutation_hz_ceiling = "scaling_commutation_hz_ceiling"
        assert scaling_commutation_hz_ceiling in brushless_drive_entries
        #TODO: find valid range of values for scaling_commutation_hz_ceiling
        new_scaling_commutation_hz_ceiling = 31000
        print(f"\nSetting {scaling_commutation_hz_ceiling} to {new_scaling_commutation_hz_ceiling}")
        status = vertiq_8108.set_verify(brushless_drive, scaling_commutation_hz_ceiling, new_scaling_commutation_hz_ceiling)
        print(f"status: {status}")
        assert status is True

        scaling_commutation_hz_floor = "scaling_commutation_hz_floor"
        assert scaling_commutation_hz_floor in brushless_drive_entries
        #TODO: find valid range of values for scaling_commutation_hz_floor
        new_scaling_commutation_hz_floor = 17000
        print(f"\nSetting {scaling_commutation_hz_floor} to  {new_scaling_commutation_hz_floor}")
        status = vertiq_8108.set_verify(brushless_drive, scaling_commutation_hz_floor, new_scaling_commutation_hz_floor)
        print(f"status: {status}")
        assert status is True

        scaling_commutation_cycles_per_erev = "scaling_commutation_cycles_per_erev"
        assert scaling_commutation_cycles_per_erev in brushless_drive_entries
        #TODO: find valid range of values for scaling_commutation_cycles_per_erev
        new_scaling_commutation_cycles_per_erev = 60
        print(f"\nSetting {scaling_commutation_cycles_per_erev} to {new_scaling_commutation_cycles_per_erev}")
        status = vertiq_8108.set_verify(brushless_drive, scaling_commutation_cycles_per_erev, new_scaling_commutation_cycles_per_erev)
        print(f"status: {status}")
        assert status is True


    def test_esc_propeller_input_parser(self, vertiq_8108, client_list):
        esc_propeller_input_parser = "esc_propeller_input_parser"
        assert esc_propeller_input_parser in client_list

        esc_propeller_input_parser_entries = vertiq_8108.return_client_entries(esc_propeller_input_parser)
        assert esc_propeller_input_parser_entries is not None

        thrust_max = "thrust_max"
        print(f"\nConfirming {thrust_max} is removed from {esc_propeller_input_parser}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(esc_propeller_input_parser, thrust_max)

    def test_hobby_input(self, vertiq_8108, client_list):
        hobby_input = "hobby_input"
        assert hobby_input in client_list

        hobby_input_entries = vertiq_8108.return_client_entries(hobby_input)
        assert hobby_input_entries is not None

        hobby_telemetry_frequency = "hobby_telemetry_frequency"
        assert hobby_telemetry_frequency in hobby_input_entries
        new_hobby_telemetry_frequency = 1000
        print(f"\nSetting {hobby_telemetry_frequency} to {new_hobby_telemetry_frequency}")
        status = vertiq_8108.set_verify(hobby_input, hobby_telemetry_frequency, new_hobby_telemetry_frequency)
        print(f"status: {status}")
        assert status is True

        hobby_telemetry_speed_style = "hobby_telemetry_speed_style"
        assert hobby_telemetry_speed_style in hobby_input_entries
        new_hobby_telemetry_speed_style = 1
        print(f"\nSetting {hobby_telemetry_speed_style} to {new_hobby_telemetry_speed_style}")
        status = vertiq_8108.set_verify(hobby_input, hobby_telemetry_speed_style, new_hobby_telemetry_speed_style)
        print(f"status: {status}")
        assert status is True

        allow_dshot_disarming_message = "allow_dshot_disarming_message"
        assert allow_dshot_disarming_message in hobby_input_entries
        new_allow_dshot_disarming_message = 0
        print(f"\nSetting {allow_dshot_disarming_message} to {new_allow_dshot_disarming_message}")
        status = vertiq_8108.set_verify(hobby_input, allow_dshot_disarming_message, new_allow_dshot_disarming_message)
        print(f"status: {status}")
        assert status is True


    def test_propeller_motor_control(self, vertiq_8108, client_list):
        propeller_motor_control = "propeller_motor_control"
        assert propeller_motor_control in client_list

        propeller_motor_control_entries = vertiq_8108.return_client_entries(propeller_motor_control)
        assert propeller_motor_control_entries is not None

        ctrl_thrust = "ctrl_thrust"
        print(f"\nConfirming {ctrl_thrust} is removed from {propeller_motor_control}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(propeller_motor_control, ctrl_thrust)

        propeller_kt_pos = "propeller_kt_pos"
        print(f"\nConfirming {propeller_kt_pos} is removed from {propeller_motor_control}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(propeller_motor_control, propeller_kt_pos)

        propeller_kt_neg = "propeller_kt_neg"
        print(f"\nConfirming {propeller_kt_neg} is removed from {propeller_motor_control}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(propeller_motor_control, propeller_kt_neg)

    def test_multi_turn_angle_control(self, vertiq_8108, client_list):
        multi_turn_angle_control = "multi_turn_angle_control"
        assert multi_turn_angle_control in client_list

        multi_turn_angle_control_entries = vertiq_8108.return_client_entries(multi_turn_angle_control)
        assert multi_turn_angle_control_entries is not None

        low_power_hold_allowed_target_error = "low_power_hold_allowed_target_error"
        new_low_power_hold_allowed_target_error = 0.05
        print(f"\nSetting {low_power_hold_allowed_target_error} to {new_low_power_hold_allowed_target_error}")
        status = vertiq_8108.set_verify(multi_turn_angle_control, low_power_hold_allowed_target_error, new_low_power_hold_allowed_target_error)
        print(f"status: {status}")
        assert status is True

        low_power_hold_max_brake_error = "low_power_hold_max_brake_error"
        new_low_power_hold_max_brake_error = 0.05
        print(f"\nSetting {low_power_hold_max_brake_error} to {new_low_power_hold_max_brake_error}")
        status = vertiq_8108.set_verify(multi_turn_angle_control, low_power_hold_max_brake_error, new_low_power_hold_max_brake_error)
        print(f"status: {status}")
        assert status is True

        ctrl_angle_low_power = "ctrl_angle_low_power"
        new_ctrl_angle_low_power = 0.05
        print(f"\nSetting {ctrl_angle_low_power} to {new_ctrl_angle_low_power}")
        status = vertiq_8108.set_verify(multi_turn_angle_control, ctrl_angle_low_power, new_ctrl_angle_low_power)
        print(f"status: {status}")
        assert status is True

    def test_arming_handler(self, vertiq_8108, client_list):
        arming_handler = "arming_handler"
        assert arming_handler in client_list

        arming_handler_entries = vertiq_8108.return_client_entries(arming_handler)
        assert arming_handler_entries is not None

        manual_arming_throttle_source = "manual_arming_throttle_source"
        print(f"\nConfirming {manual_arming_throttle_source} is removed from {arming_handler}")
        with pytest.raises(iqmotion.custom_errors.IqModuleError):
            vertiq_8108.get(arming_handler, manual_arming_throttle_source)

        play_arming_song_on_arm = "play_arming_song_on_arm"
        new_play_arming_song_on_arm = 0
        print(f"\nSetting {play_arming_song_on_arm} to {arming_handler}")
        status = vertiq_8108.set_verify(arming_handler, play_arming_song_on_arm, new_play_arming_song_on_arm)
        print(f"status: {status}")
        assert status is True

    def test_reboot_module(self, vertiq_8108):
        print(f"\nRebooting module")
        system_control = "system_control"
        reboot_program = "reboot_program"

        vertiq_8108.set(system_control, reboot_program)
        time.sleep(3)
        status = vertiq_8108.get(system_control, "module_id")
        assert status is not None

