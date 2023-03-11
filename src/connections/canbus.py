from .j2534_connection import J2534Connection

import can
import struct
import time
import sys

class CANBUS:
    def __init__(self):
        is_windows = sys.platform.startswith('win')
        if is_windows:
            self.bus = J2534Connection()
            self.bus.open()
            pass
        else:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")

        self.debug = False
    def can_send(self,addr, dat, timeout):
        msg = can.Message(
            arbitration_id=addr, data=dat, is_extended_id=False
        )
        self.bus.send(msg,timeout)
        pass
    def can_recv(self,timeout = 1):
        message = self.bus.recv(timeout) 
        if message is None:
            self.print('Timeout occurred, no message.')
        ret = []
        ret.append((message.arbitration_id, 0, message.data, 0))
        return ret
        pass
    def print(self,*args):
        if self.debug:
            print(args)