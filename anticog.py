import iqmotion as iq
import threading
import sys

mot = iq.RdModule()

anticog = True
SECONDS = 3.0

def toggle_anticogging():
    global anticog, mot
    anticog = not anticog
    mot.set("anticogging_pro", "enabled", anticog)
    print("We are printing from a thread")


if __name__ == '__main__':
   
    mot.ramp_volts(2,2)

    while True:
        try:
            timer = threading.Timer(SECONDS, toggle_anticogging)
            timer.start()
            timer.join()
        except KeyboardInterrupt:
            mot.coast()
            sys.exit()