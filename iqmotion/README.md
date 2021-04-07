# IQ Modules

## Creating a Vertiq Module

Currently IQ Python API supports 2 motors: Vertiq 2306 & Vertiq 8108

Here's how you create a Vertiq Module:  

```python
import iqmotion as iq

serial_port = "/dev/ttyUSB0" # Machine dependent
com = iq.SerialCommunicator(serial_port)

# Create a vertiq2306 module with default firmware settings ("speed")
vertiq2306 = iq.Vertiq2306(com, 0)

# Create a vertiq8108 module with default firmware settings ("speed")
vertiq8108 = iq.Vertiq8108(com, 0) 
```

## Choosing the firmware for the Vertiq Module

If you have flashed different firmware onto the module, then you'll need to reflect that change in the API as well.  

* The Vertiq2306 currently supports:  
    `firmware = ["stepdir", "speed", "servo"]`

* The Vertiq8108 currently supports:  
    `firmware = ["speed"]`

Here's how you change the firmware in the API

```python
# Create a vertiq module with different firmare settings
vertiq2306 = iq.vertiq2306(com, 0, firmware="stepdir") 
```

## Load new clients on top of your Vertiq Module

To add clients on top of a Vertiq2306 or Vertiq8108, create a folder that holds all of your custom client json files and pass the folder name to the module.

```python
# This folder should contain custom client jsons
clients_path = "clients/" 

vertiq2306 = iq.vertiq2306(com, 0, clients_path=clients_path)
vertiq2306.list_clients() # Displays loaded clients for the module
```

## Create a Base Module containing only essential clients

A Base Module is a module that contains all the essentials clients needed to interact with a motor. It does not have any control modules so it's a blank slate.

To start with a base module and add clients on top, create a folder that holds all of your custom client json files and pass the folder name to the module.

```python
# This folder should contain custom client jsons
clients_path = "custom_clients/"

FlyDronePro = iq.BaseIqModule(com, 0, clients_path=clients_path)
FlyDronePro.list_clients() # Displays loaded clients for the module
```

