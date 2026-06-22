import time
import iqmotion as iq

# Test 1: Get All on relevant hyperdrive endpoints with the Vspin Module
# com = iq.SerialCommunicator("COM3", baudrate=115200)
# vertiq = iq.VSpinG2Module(com=com)
#
# print(vertiq.get_all("system_control"))
# print(vertiq.get_all("motor_model"))
# print(vertiq.get_all("motor_driver"))
# print(vertiq.get_all("field_weakening_controller"))
# print(vertiq.get_all("current_safeties"))
# print(vertiq.get_all("propeller_motor_control"))
# print(vertiq.get_all("drive_control_interface"))
# print(vertiq.get_all("voltage_target_generator"))
# print(vertiq.get_all("rotor_angle_generator"))


# Test 2: Does the RDModule work?
# vertiq = iq.RdModule(port="COM3")
# print(vertiq.get_all("system_control"))
# print(vertiq.get_all("motor_model"))
# print(vertiq.get_all("field_weakening_controller"))


# Test 3: Does ramping and coasting with the RDModule work?
# vertiq = iq.RdModule(port="COM3")
#
# vertiq.ramp_volts(10.0, 5.0)
# print(vertiq.get("motor_driver", "stator_magnitude"))
# vertiq.coast()
# time.sleep(5)
#
# vertiq.ramp_velocity(100.0, 5.0)
# print(vertiq.get("motor_model", "mechanical_velocity"))
# vertiq.coast()


# Test 4: Does ramping and coasting with the VSpin module work?
# com = iq.SerialCommunicator("COM3", baudrate=115200)
# vertiq = iq.VSpinG2Module(com=com)
#
# vertiq.ramp_volts(10.0, 5.0)
# print(vertiq.get("motor_driver", "stator_magnitude"))
# vertiq.coast()
# time.sleep(5)
#
# vertiq.ramp_velocity(100.0, 5.0)
# print(vertiq.get("motor_model", "mechanical_velocity"))
# vertiq.coast()

# Test 5: Do set verifies work with the new module? Tests setting and getting
# com = iq.SerialCommunicator("COM3", baudrate=115200)
# vertiq = iq.VSpinG2Module(com=com)
#
# starting_ke = vertiq.get("motor_model", "mechanical_ke_at_20c")
# ending_ke = starting_ke + (starting_ke * 0.05)
#
# print(f"Starting Ke: {starting_ke}")
# print(f"Ending Ke: {ending_ke}")
# verified = vertiq.set_verify("motor_model", "mechanical_ke_at_20c", ending_ke)
# assert verified
# print("Ke change verified")
