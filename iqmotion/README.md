# How to Add new Clients and Client Entries for R&D

## Step 1: Create A New Module JSON File

**Make sure this file is placed in the directory: `iqmotion/module_files`**

For Example: If the R&D Servo Firmware has a new client called `crazy_new_feature`, we will want to create a json file (`servo_rd_module.json` ) that contains the new client:

```json
{
  "clients": [
    "crazy_new_feature", <------- (New client)
    "brushless_drive",
    "multi_turn_angle_control",
    "anticogging",
    "buzzer_control",
    "hobby_input",
    "persistent_memory",
    "power_monitor",
    "serial_interface",
    "servo_input_parser",
    "system_control",
    "temperature_estimator",
    "temperature_monitor_uc"
  ]
}
```

## Step 2: Create Client Entry JSON for any new clients

Create a new client_entry json (`crazy_new_feature.json`) that holds the client entries for the client.

**Make sure this file is placed in the directory: `iqmotion/module_files`**

```json
[
{"type_idn":11, "param":"new_feature_value1", "param_idn":  0, "format":"", "unit": ""},
{"type_idn":11, "param":"new_feature_value2", "param_idn":  1, "format":"", "unit": ""}
]
```
