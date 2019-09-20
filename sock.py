#!/usr/bin/env python3

from socket import socket
from socket import AF_INET, SOCK_STREAM
from selectors import DefaultSelector, EVENT_READ
from threading import Thread
from lsocket.buffer import Buffer
from time import sleep as _sleep

class lsocket(socket):

    def __init__(self, *args, **kwargs):
        super().__init__(AF_INET, SOCK_STREAM)
        self._buffer = Buffer()

    def connect(self, host, port):
        super().connect((host, port))

        super().setblocking(False)

        selector = DefaultSelector()
        selector.register(self, EVENT_READ, self._buffer.extend)
        Thread(target=self._read_forever,
            args=(selector,),
            daemon=True).start()


    def _read_forever(self, selector):
        while True:
            events = selector.select()

            data = super().recv(4096)
            self._buffer.extend(data)

    def recvuntil(self, msg):
        while True:
            data = self._buffer.consume_until(msg)

            if data:
                return data

            _sleep(0.2)

        return None

    def recvline(self, line='\n'):
        return self.recvuntil(line)

    def sendline(self, msg):
        msg += '\n'
        super().send(msg.encode())
