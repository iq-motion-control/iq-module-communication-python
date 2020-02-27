import iqmotion as iq
import time
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", help="serial port name where the iq module is connected"
    )
    args = parser.parse_args()
    if args.port:
        print("verbosity turned on")

    com = iq.SerialCommunicator("/dev/ttyUSB0")
    iq_module = iq.SpeedModule(com, 0)

    MAX_SPEED = 50
    SPEED_STEP = 1

    velocity_to_set = 0
    velocity_sign = 1

    while True:

        # Update velocity direction
        if abs(velocity_to_set) >= MAX_SPEED:
            velocity_sign *= -1

        # Increase velocity
        velocity_to_set += SPEED_STEP * velocity_sign
        iq_module.set("propeller_motor_control", "ctrl_velocity", velocity_to_set)

        # Limit acceleration at a constant rate
        time.sleep(0.2)

