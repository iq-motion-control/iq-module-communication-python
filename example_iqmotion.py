import iqmotion as iq
from datetime import datetime
from time import sleep

com = iq.SerialCommunicator("COM4", baudrate=115200)

vertiq = iq.SpeedModule(com, 0)
# vertiq = iq.HyperdriveSpeedModule(com=com, module_id=0)
# vertiq.add_client(client_file_path="iqmotion/clients/client_files/motor_model.json")
# vertiq.add_client(client_file_path="iqmotion/clients/client_files/drive_control_interface.json")
# vertiq = iq.SpeedModule(com, 63)

# vertiq.set("system_control", "module_id", 0)
# vertiq.save("system_control", "module_id")
# module_id = vertiq.get("system_control", "module_id")
# M28
# vertiq.set("system_control", "hardware_version", 1835008)
# vertiq.set("system_control", "electronics_version", 1048576)
# M626
# vertiq.set("system_control", "hardware_version", 41025536)
# vertiq.set("system_control", "electronics_version", 41025536)

# M40.256
# vertiq.set("system_control", "hardware_version", 2621696)
# E21.256
# vertiq.set("system_control", "electronics_version", 1376512)



# vertiq.save("system_control", "hardware_version")
# vertiq.save("system_control", "electronics_version")


# sleep(1)
# print(vertiq.get("system_control", "hardware_version"))
# print(vertiq.get("system_control", "electronics_version"))
# print(vertiq.get("system_control", "firmware_version"))
# print(vertiq.get("system_control", "firmware_valid"))
# # print(vertiq.get("brushless_drive", "derate_low_pass_filter_fc"))
#
build_year = vertiq.get('system_control', 'build_year')
build_month = vertiq.get('system_control', 'build_month')
build_day = vertiq.get('system_control', 'build_day')
build_date_string = f"{build_year}/{build_month}/{build_day}"
build_date = datetime.strptime(build_date_string, "%Y/%m/%d")

print(f"build_year: {build_year}")
print(f"build_month: {build_month}")
print(f"build_day: {build_day}")
#
# wanted_build_year = 2024
# wanted_build_month = 9
# wanted_build_day = 25
# wanted_build_date_string = f"{wanted_build_year}/{wanted_build_month}/{wanted_build_day}"
# wanted_build_date = datetime.strptime(wanted_build_date_string, "%Y/%m/%d")

# if build_date < wanted_build_date:
#     print(f"build date less than wanted build date")
# else:
#     print(f"build date greater than wanted build date")
#
# vertiq.set("arming_handler", "consecutive_disarming_throttles_to_disarm", 0)
# vertiq.save("arming_handler", "consecutive_disarming_throttles_to_disarm")

# print(vertiq.get("arming_handler", "consecutive_disarming_throttles_to_disarm", 0))

# vertiq.set("system_control", "reboot_boot_loader")
# print(module_id)


vertiq.ramp_velocity(400, 5.0)
# print(vertiq.get("motor_model", "mechanical_velocity"))
# print(vertiq.get("brushless_drive", "obs_velocity"))
vertiq.ramp_velocity(0, 5.0)
vertiq.coast()
vertiq.ramp_volts(5, 5.0)
# print(vertiq.get("drive_control_interface", "voltage_target"))
# print(vertiq.get("brushless_drive", "drive_volts"))
vertiq.ramp_volts(0, 5.0)
vertiq.coast()
vertiq.ramp_volts_slew(5, 5.0)
vertiq.ramp_volts_slew(0, 5.0)
vertiq.coast()
