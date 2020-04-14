from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.iq_devices.ramper import Ramper


class SpeedModule(IqModule):
    """ Creates SpeedModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
    """

    _MODULE_FILE_NAME = "speed.json"

    def ramp_velocity(self, final_velocity: float, total_time: float, time_steps=20):
        velocity_client = "propeller_motor_control"
        velocity_client_entry = "ctrl_velocity"
        success = Ramper.ramp_velocity(
            self,
            velocity_client,
            velocity_client_entry,
            final_velocity,
            total_time,
            time_steps,
        )

        return success

    def ramp_volts(self, final_volts: float, total_time: float, time_steps=20):
        volts_client = "propeller_motor_control"
        volts_client_entry = "ctrl_volts"
        success = Ramper.ramp_volts(
            self, volts_client, volts_client_entry, final_volts, total_time, time_steps,
        )

        return success

    def ramp_volts_slew(self, final_volts: float, slew_rate: float):
        success = Ramper.ramp_volts_slew(self, final_volts, slew_rate)

        return success
