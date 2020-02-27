import iqmotion as iq
import math


def send_tranjectory(iq_module, time_cmd, angle_cmd):
    iq_module.set(
        "multi_turn_angle_control", "trajectory_angular_displacement", angle_cmd
    )

    iq_module.set("multi_turn_angle_control", "trajectory_duration", time_cmd)


if __name__ == "__main__":
    com = iq.SerialCommunicator("/dev/ttyUSB0")
    iq_module = iq.ServoModule(com, 0)

    START_ANGLE = iq_module.get("multi_turn_angle_control", "obs_angular_displacement")
    ANGLE = START_ANGLE + (12 * math.pi)
    TIME = 5

    # Set custom PID values
    iq_module.set("multi_turn_angle_control", "angle_Kp", 0.5)
    iq_module.set("multi_turn_angle_control", "angle_Ki", 0)
    iq_module.set("multi_turn_angle_control", "angle_Kd", 0)

    # Send First Trajectory
    send_tranjectory(iq_module, TIME, ANGLE)
    spin_direction = -1

    while True:

        # Wait until module has finish his last trajectory
        # If communication fails, "get()" returns a None
        mode = None
        while mode == 6 or mode == None:
            mode = iq_module.get("multi_turn_angle_control", "ctrl_mode")

        # Send a new trajectory
        if spin_direction == 1:
            send_tranjectory(iq_module, TIME, ANGLE)
        else:
            send_tranjectory(iq_module, TIME, START_ANGLE)

        spin_direction *= -1
