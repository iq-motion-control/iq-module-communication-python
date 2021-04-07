import sys
sys.path.append('../')

import iqmotion as iq
import time
import math

# Motor Comms
com = iq.SerialCommunicator("/dev/ttyUSB2") # Q-Motor

# Clients to Load
client_files = "clients/"

# Create a custom Module
FlyIQ = iq.BaseIqModule(com, 0, client_files)
FlyIQ.list_clients()

# Using the Vertiq8108 with additional custom client files
vertiq8108 = iq.Vertiq8108(com, 0, firmware="speed", clients_path=client_files)
vertiq8108.list_clients()

# Using the Vertiq2306 with additional custom client files
vertiq2306 = iq.Vertiq2306(com, 0, firmware="stepdir", clients_path=client_files)


