import sys
sys.path.append('../')

import iqmotion as iq
import time
import math

# Motor Comms
Qcom = iq.SerialCommunicator("/dev/ttyUSB0") # Q-Motor

# Motor Modules    
Q = iq.CustomIqModule("module_files/servo_rd_module.json", Qcom, extra_clients=["extra_clients_files/crazy_new_feature"])


