from iqmotion.iq_devices.iq_module import IqModule

import numpy as np
import time


class Ramper:
    @staticmethod
    def ramp_velocity(
        iq_module: IqModule,
        velocity_client: str,
        velocity_client_entry: str,
        final_velocity: float,
        total_time: float,
        time_steps=20,
    ):
        init_velocity = iq_module.get_retry(
            "brushless_drive", "obs_velocity", retries=5
        )

        if init_velocity == None:
            return 0

        num_steps = round(1000 * total_time / time_steps)  # 20ms time steps by default

        velocity_steps = np.linspace(init_velocity, final_velocity, num_steps)
        time_steps = np.linspace(0, total_time, num_steps)

        start_time = time.perf_counter()
        for step in range(num_steps):
            while time.perf_counter() < start_time + time_steps[step]:
                pass
            new_velocity = velocity_steps[step]
            iq_module.set(velocity_client, velocity_client_entry, new_velocity)

        return 1

    @staticmethod
    def ramp_volts(
        iq_module: IqModule,
        volts_client: str,
        volts_client_entry: str,
        final_volts: float,
        total_time: float,
        time_steps=20,
    ):
        init_volts = iq_module.get_retry("brushless_drive", "drive_volts", retries=5)

        if init_volts == None:
            return 0

        num_steps = int(
            round(1000 * total_time / time_steps)
        )  # 20ms time steps by default

        volts_steps = np.linspace(init_volts, final_volts, num_steps)
        time_steps = np.linspace(0, total_time, num_steps)

        start_time = time.perf_counter()
        for step in range(num_steps):
            while time.perf_counter() < start_time + time_steps[step]:
                pass
            new_voltage = volts_steps[step]
            iq_module.set(volts_client, volts_client_entry, new_voltage)

        return 1

    @staticmethod
    def ramp_volts_slew(iq_module: IqModule, final_volts: float, slew_rate: float):
        init_volts = iq_module.get_retry("brushless_drive", "drive_volts", retries=5)

        if init_volts == None:
            return 0

        time = abs((final_volts - init_volts) / slew_rate)

        success = iq_module.ramp_volts(final_volts, time)
        return success
