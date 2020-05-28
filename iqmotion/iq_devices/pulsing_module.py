from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.iq_devices.common_commands.ramper import Ramper


class PulsingModule(IqModule):
    """ Creates PulsingModule object
    
    Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
    """

    _DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
    _MODULE_FILE_NAME = "pulsing.json"

    def ramp_velocity(self, final_velocity: float, total_time: float, time_steps=20):
        """ Ramps velocity of the module up to a target in set amount of seconds

        Arguments:
            final_velocity {float} -- final velocity goal
            total_time {float} -- time to reach velocity goal (s)

        Keyword Arguments:
            time_steps {int} -- num of velocity increments (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        velocity_client = self._DEFAULT_CONTROL_CLIENT
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
        """ Ramps the volts of the module up to a target in set amount of seconds

        Arguments:
            final_volts {float} -- final volts goal
            total_time {float} -- time to reach volts goal (s)

        Keyword Arguments:
            time_steps {int} -- num of volts increment (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        volts_client = self._DEFAULT_CONTROL_CLIENT
        volts_client_entry = "ctrl_volts"
        success = Ramper.ramp_volts(
            self, volts_client, volts_client_entry, final_volts, total_time, time_steps,
        )

        return success

    def ramp_volts_slew(self, final_volts: float, slew_rate: float):
        """ Ramps the volts of the module up to a target following a slew rate

        Arguments:
            final_volts {float} -- final volts goal
            slew_rate {float} -- wanted slew rate

        Returns:
            bool -- True if the ramp was successful
        """
        success = Ramper.ramp_volts_slew(self, final_volts, slew_rate)

        return success
