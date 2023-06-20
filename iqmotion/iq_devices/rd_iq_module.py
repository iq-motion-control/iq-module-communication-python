from iqmotion.iq_devices.iq_module import IqModule
from iqmotion.communication.serial_communicator import SerialCommunicator
from iqmotion.custom_errors import CommunicationError, IqModuleError
from iqmotion.iq_devices.utils import get_parent_dir, load_all_clients

import os
import sys
import glob
import serial

SPEED   = '1'
SERVO   = '2'
STEPDIR = '4'

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
        style: str = None,      
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
        elif len(ports_avail) == 1:
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

        # Try to automagically figure out the firmware style
        firmware_version = self.get("system_control", "firmware_version")
        firmware_style = str(0xFFFF & (firmware_version >> 20))
        if (style=="speed" or firmware_style == SPEED):
            self._DEFAULT_CONTROL_CLIENT = "propeller_motor_control"
        elif(style=="position" or firmware_style == SERVO or firmware_style == STEPDIR):
            self._DEFAULT_CONTROL_CLIENT = "multi_turn_angle_control"
        else:
            err_msg = "Please select the motor firmware style:\n\n"
            err_msg += "'speed' or 'position'"
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