from .j2534_connection import J2534Connection

import can
import struct
import time
import sys
from collections import namedtuple

class CAN_MESSAGE():
    def __init__(self,id,data):
        self.id = id
        self.data = data
    def __str__(self):
        return "Can Message " + str(self.id) + " " + self.data.hex()
    

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
    def can_recv(self,timeout = 1) -> CAN_MESSAGE:
        message = self.bus.recv(timeout) 
        if(message is not None):
            message = CAN_MESSAGE(message.arbitration_id,message.data)
        return message

    def print(self,*args):
        if self.debug:
            print(args)