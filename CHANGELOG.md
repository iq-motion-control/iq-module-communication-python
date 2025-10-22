# Changelog
Note: version releases in the 0.x.y range may introduce breaking changes.

## 0.29.1

- patch: Addec coil_temperature_estimator for Servo module

## 0.29.0

- minor: Updated client entries

## 0.28.0

- minor: Improved hyperdrive support for R&D and updated client_files

## 0.27.0

- minor: Update client_files and added support for hyperdrive in RdModule

## 0.26.1

- patch: Updated client files

## 0.26.0

- minor: Added new module files and updated existing ones with new clients. Added bugfixes to RdModule.

## 0.25.0

- minor: Hypderdrive support and RdModule improvements

## 0.24.2

- patch: Updated client files

## 0.24.1

- patch: Fixed typo in disarm_behavior in arming_handler

## 0.24.0

- minor: Added LED support and updated rd module

## 0.23.0

- minor: Added Vertiq6008 module

## 0.22.0

- minor: Added power_safety client, 40-06 servo and speed module files, and more test files for 23-06 and 40-06

## 0.21.13

- patch: Test client_files sync

## 0.21.12

- patch: Testing again

## 0.21.11

- patch: Undo overwrite url

## 0.21.10

- patch: Testing fix for relative path again

## 0.21.9

- patch: Testing again

## 0.21.8

- patch: Testing fix for submodule path

## 0.21.7

- patch: Testing ssh key again

## 0.21.6

- patch: Testing ssh key for client_files

## 0.21.5

- patch: Testing fix for username bug

## 0.21.4

- patch: Testing relative paths

## 0.21.3

- patch: Testing initializing submodule

## 0.21.2

- patch: Testing fix in MANIFEST.in

## 0.21.1

- patch: Fixing packages

## 0.21.0

- minor: Testing client_files submodule

## 0.20.0

- minor: Once again trying to fix pypi versioning issue

## 0.19.0

- minor: Placeholder again to fix pypi version due to permissions issue

## 0.18.0

- minor: Placeholder to fix pypi version due to permissions issue

## 0.17.0

- minor: Placeholder to fix pypi version

## 0.16.0

- minor: Added new 4006 module and updated endpoints for system_control

## 0.15.1

- patch: Update client files for 8108 servo

## 0.15.0

- minor: Added new clients for 81-08 speed, fortiq, and pulsing

## 0.14.2

- patch: Fix unit fields for power_safety

## 0.14.1

- patch: Fix param_idn fields in power_safety

## 0.14.0

- minor: Added power_safety client

## 0.13.1

- patch: Undo derate name change in brushless_drive

## 0.13.0

- minor: Update anticogging_pro, brushless_drive, hobby_input, persistent_memory, power_monitor, serial_interface, servo_input_parser, system_control, temperature_esimator, and uavcan_node

## 0.12.0

- minor: Update persistent_memory client file

## 0.11.13

- patch: Patched RD module to work with Windows

## 0.11.12

- patch: Updated Vertiq8108 Files

## 0.11.11

- patch: compress rd module code

## 0.11.10

- patch: remove the local toml file

## 0.11.9

- patch: get_all_retry bug fix

## 0.11.8

- patch: modified anticogging_pro

## 0.11.7

- patch: You can now change the baudrate from within the module using .update_baudrate

## 0.11.6

- patch: Added Anticogging_ft client to main code base

## 0.11.5

- patch: internal update 2

## 0.11.4

- patch: Internal Update

## 0.11.3

- patch: Exposes CustomIQModule through iq import

## 0.11.2

- patch: Restored CustomIQModule

## 0.11.1

- patch: Updated Coverage tests for the New Vertiq's, Fortiq's, and Base Modules

## 0.11.0

- minor: updated modules and clients for vertiq2306 and vertiq8108

## 0.10.0

- minor: updated clients for new firmware speed v23 and servo v15

## 0.9.3

- patch: fix set_verify for multiple values bug

## 0.9.2

- patch: fixed multiple values for set bug

## 0.9.1

- patch: values for get/set are now list instead of *args, set_verify retries the set as well, flushes input com before each retry

## 0.9.0

- minor: added get with value support and multiple set values

## 0.8.0

- minor: handles custom modules and dynamically adding clients

## 0.7.0

- minor: coast() method now available for modules

## 0.6.1

- patch: adding msg variable to Custom Error Base Class

## 0.6.0

- minor: Custom Error Base Class

## 0.5.0

- minor: added set_verify and get_all_retry, updated rampers docstring

## 0.4.0

- minor: added hardware testing, fixed ramp_to_volts

## 0.3.0

- minor: fixed parsing issues, adding pulsing, adding ramping methods

## 0.2.1

- patch: added modules

## 0.2.0

- minor: Update client and module files

## 0.1.0

- minor: Initial Release

