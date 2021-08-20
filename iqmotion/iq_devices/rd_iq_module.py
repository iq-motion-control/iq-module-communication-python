from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.serial_communicator import SerialCommunicator
from iqmotion.custom_errors import CommunicationError, IqModuleError
from iqmotion.iq_devices.utils import get_parent_dir, load_all_clients

import os
import sys
import glob
import serial

class RdModule(IqModule):
    """ Creates R&D Object with every publicly available json

    The R&D Module does a few things different than other modules:

        1. Creates dynamic json that contains all the public facing clients
        2. Automatically connects to serial com port
            Will throw an error if more than one serial port exists and one wasn't provided
    
    Optional Arguments:
        com {Communicator} -- The communicator object to interface with the IqModule
        port {str} -- will connect to this port if more than one port is detected
    
    Keyword Arguments:
        module_idn {int} -- The idn of the module (default: {0})
        extra_clients {list} -- list of file paths to extra clients you want to load in the module (default: {None})
    """

    def __init__(
        self,
        port: str=None,
        baudrate: int=115200,
        module_idn: int = 0,      
        clients_path: str = None
    ):
        
        self._DEFAULT_VELOCITY_CLIENT_ENTRY = "ctrl_velocity"
        self._DEFAULT_VOLTS_CLIENT_ENTRY = "ctrl_volts"
        self._MODULE_FILE_NAME = "rd.json"


        # Dynamically Load all clients into one module file
        path = os.path.join(get_parent_dir(__file__, 2), "clients/client_files")
        rd = os.path.join(os.path.dirname(__file__), "module_files/rd.json")
        clients = load_all_clients(path)
        
        # Load them into a RD Module file
        with open(rd, 'w') as f:
            f.write(clients)

        # Pull all the available ports into a list
        ports_avail = self._find_serial_ports()

        # Let user decide which port they want
        if port is not None:
            com = SerialCommunicator(port, baudrate)
        # Otherwise allow RdModule auto-connect if it's only 1 port open
        if len(ports_avail) == 1:
            port = ports_avail[0]
            com = SerialCommunicator(port, baudrate)
        # If too many ports are available, you should pass one in
        elif len(ports_avail) > 1:
            err_msg = "Too many ports available to choose from, "
            err_msg += "Please choose one of the following:\n\n"
            err_msg += f"{ports_avail}\n"
            err_msg += "ex: motor = iq.RdModule(port='COM1', baudrate=115200)"
            raise CommunicationError(err_msg)    
        # No ports available
        else:
            err_msg = "No available ports detected"
            raise CommunicationError(err_msg)
        

        super().__init__(com, module_idn, clients_path)

    def ramp_propeller_velocity(self, final_velocity: float, total_time: float, time_steps=20):
        """ Ramps Velocity of the module up via Propeller Client to a target in set amount of seconds

        Arguments:
            final_velocity {float} -- final velocity goal
            total_time {float} -- time to reach velocity goal (s)

        Keyword Arguments:
            time_steps {int} -- num of velocity increments (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """

        self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
        success = super().ramp_velocity(final_velocity, total_time, time_steps)
        
        return success

    def ramp_multi_turn_velocity(self, final_velocity: float, total_time: float, time_steps=20):
        """ Ramps Velocity of the module up via Multi Turn Client to a target in set amount of seconds

        Arguments:
            final_velocity {float} -- final velocity goal
            total_time {float} -- time to reach velocity goal (s)

        Keyword Arguments:
            time_steps {int} -- num of velocity increments (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """

        self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
        success = super().ramp_velocity(final_velocity, total_time, time_steps)
        
        return success

    def ramp_velocity(self, final_velocity: float=None, total_time: float=None, time_steps=None):
        """ NOT SUPPORTED 

            Please use ramp_multi_turn_velocity or ramp_propeller_velocity
        """
        err_msg = "ramp_velocity not supported with Rd_module:\n\n"
        err_msg += "Please use ramp_multi_turn_velocity or ramp_propeller_velocity"
        raise IqModuleError(err_msg)

    def coast_prop(self):
        """ Send a coast command to the propeller motor control client 
        
        """
        self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
        super().coast()

    def coast_multi_turn(self):
        """ Send a coast command to the multi turn angle control client
        
        """
        self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
        super().coast()

    def coast(self):
        """ NOT SUPPORTED 

            Please use coast_multi_turn or coast_prop
        """
        err_msg = "coast not supported with Rd_module:\n\n"
        err_msg += "Please use coast_multi_turn or coast_prop"
        raise IqModuleError(err_msg)

    def ramp_multi_turn_volts(self, final_volts: float, total_time: float, time_steps=20):
        """ Ramps the volts of the module via multi_turn client up to a target in set amount of seconds

        Arguments:
            final_volts {float} -- final volts goal
            total_time {float} -- time to reach volts goal (s)

        Keyword Arguments:
            time_steps {int} -- num of volts increment (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
        return super().ramp_volts(final_volts, total_time, time_steps=time_steps)

    def ramp_propeller_volts(self, final_volts: float, total_time: float, time_steps=20):
        """ Ramps the volts of the module via Propeller client up to a target in set amount of seconds

        Arguments:
            final_volts {float} -- final volts goal
            total_time {float} -- time to reach volts goal (s)

        Keyword Arguments:
            time_steps {int} -- num of volts increment (default: {20})

        Returns:
            bool -- True if the ramp was successful
        """
        self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
        return super().ramp_volts(final_volts, total_time, time_steps=time_steps)

    def ramp_volts(self, final_volts: float=None, total_time: float=None, time_steps=None):
        """ NOT SUPPORTED 

            Please use ramp_multi_turn_volts or ramp_propeller_volts
        """
        err_msg = "ramp_volts not supported with Rd_module:\n\n"
        err_msg += "Please use ramp_multi_turn_volts or ramp_propeller_volts"
        raise IqModuleError(err_msg)

    def _find_serial_ports(self):
        """ Finds a list of open serial ports

        Raises:
            EnvironmentError: Unsupported platform

        Returns:
            list: List of str of open serial ports
        """

        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            # this excludes everything but the /dev/ttyUSB
            ports = glob.glob("/dev/tty[U-Z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

        working_ports = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                working_ports.append(port)
            except (OSError, serial.SerialException):
                pass

        return working_ports