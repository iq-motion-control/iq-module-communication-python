
import array
import asyncio
import concurrent.futures
import sys
from typing import List, Optional, Union

import serial
import time


if __name__ == "__main__":
    ser1 = serial.Serial("/dev/pts/3", 152000)
    for i in range(10):
        message = "hello" + str(i) + "\n"
        ser1.write(bytes(message, 'utf-8'))
        time.sleep(3)
