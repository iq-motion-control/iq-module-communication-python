import iqmotion as iq
import time
import sys


def progress_bar():
    toolbar_width = 40

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    for _ in range(toolbar_width):
        time.sleep(0.05)  # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")  # this ends the progress bar


if __name__ == "__main__":
    # Use the correct port name for your OS
    com = iq.SerialCommunicator("/dev/ttyUSB0")
    iq_module = iq.SpeedModule(com, 0)
    # iq_module = iq.ServoModule(com, 0)
    # iq_module = iq.StepDirModule(com, 0)

    while True:

        print("Asking module for its angle")
        # Non blocking request
        iq_module.get_async("brushless_drive", "obs_angle")

        # Do something else while module has not replied
        while not iq_module.is_fresh("brushless_drive", "obs_angle"):
            print("I'm doing something else")
            progress_bar()

            # Check and store any replies from the module
            iq_module.update_replies()

        # Get the value of the reply
        obs_angle = iq_module.get_reply("brushless_drive", "obs_angle")
        print("Module's angle = {}\n".format(obs_angle))
