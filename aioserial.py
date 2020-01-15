# Copyright 2018 Henry Chang
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import array
import asyncio
import concurrent.futures
import sys
from typing import List, Optional, Union

import serial


class AioSerial(serial.Serial):

    def __init__(
            self,
            port: Optional[str] = None,
            baudrate: int = 9600,
            bytesize: int = serial.EIGHTBITS,
            parity: str = serial.PARITY_NONE,
            stopbits: Union[float, int] = serial.STOPBITS_ONE,
            timeout: Optional[float] = None,
            xonxoff: bool = False,
            rtscts: bool = False,
            write_timeout: Optional[float] = None,
            dsrdtr: bool = False,
            inter_byte_timeout: Optional[float] = None,
            exclusive: Optional[bool] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            **kwargs):
        super().__init__(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
            xonxoff=xonxoff,
            rtscts=rtscts,
            write_timeout=write_timeout,
            dsrdtr=dsrdtr,
            inter_byte_timeout=inter_byte_timeout,
            exclusive=exclusive,
            **kwargs)
        self._loop: Optional[asyncio.AbstractEventLoop] = loop
        self._read_executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._write_executor = \
            concurrent.futures.ThreadPoolExecutor(max_workers=1)

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._loop if self._loop else asyncio.get_running_loop() \
            if sys.version_info >= (3, 7) else asyncio.get_event_loop()

    @loop.setter
    def loop(self, value: Optional[asyncio.AbstractEventLoop]):
        self._loop = value

    async def read_async(self, size: int = 1) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.read, size)

    async def read_until_async(
            self,
            expected: bytes = serial.LF,
            size: Optional[int] = None) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.read_until, expected, size)

    async def readinto_async(self, b: Union[array.array, bytearray]):
        return await self.loop.run_in_executor(
            self._read_executor, self.readinto, b)

    async def readline_async(self, size: int = -1) -> bytes:
        return await self.loop.run_in_executor(
            self._read_executor, self.readline, size)

    async def readlines_async(self, hint: int = -1) -> List[bytes]:
        return await self.loop.run_in_executor(
            self._read_executor, self.readlines, hint)

    async def write_async(
            self, data: Union[bytearray, bytes, memoryview]) -> int:
        return await self.loop.run_in_executor(
            self._write_executor, self.write, data)

    async def writelines_async(
            self, lines: List[Union[bytearray, bytes, memoryview]]) -> int:
        return await self.loop.run_in_executor(
            self._write_executor, self.writelines, lines)


async def read_and_print(ser):
    bytes_buffer = bytearray()
    while True:
        bytes_in = await ser.read_async()
        print("got dem bytes")
        bytes_buffer.extend(bytes_in)
        if b"\n" in bytes_buffer:
            print(bytes_buffer.decode())
            bytes_buffer = bytearray()

        # print((await aioserial_instance.read_async()).decode(errors='ignore'), end='', flush=True)


async def SomeMath():
    for i in range(100):
        print(i)
        i += 1
        await asyncio.sleep(10)


# async def write(ser):
#     ser.write(b"h")
#     await asyncio.sleep(1)
#     ser.write(b"e")
#     await asyncio.sleep(1)
#     ser.write(b"l")
#     await asyncio.sleep(1)
#     ser.write(b"l")
#     await asyncio.sleep(1)
#     ser.write(b"o")
#     await asyncio.sleep(1)
#     ser.write(b"\n")


async def main():
    # ser1 = serial.Serial("/dev/pts/3", 152000)
    ser2 = AioSerial(port='/dev/pts/2')
    await asyncio.gather(read_and_print(ser2), SomeMath())


if __name__ == "__main__":
    # ser1 = serial.Serial("/dev/pts/3", 152000)
    # ser.write(b"hello\n")

    # ser2 = AioSerial(port='/dev/pts/2')
    asyncio.run(main())
    print("done")
