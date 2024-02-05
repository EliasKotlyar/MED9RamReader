import logging

from .j2534_connection import J2534Connection

import can
import struct
import time
import sys
from collections import namedtuple


class CAN_MESSAGE():
    def __init__(self, id: int, data: bytearray):
        assert isinstance(id, int)
        assert isinstance(data, bytearray)
        self.id = id
        self.data = data

    def __str__(self):
        return "Can Message " + str(self.id) + " " + self.data.hex()


class CANBUS:
    def __init__(self):
        self.send_timeout = 1
        self.receive_timeout = 1
        self.logger = logging.getLogger("canbus")
        is_windows = sys.platform.startswith('win')
        if is_windows:
            self.bus = J2534Connection()
            self.bus.open()
            pass
        else:
            self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.logger.info(f"Canbus opened!")

    def can_send(self, msg: CAN_MESSAGE):
        assert isinstance(msg, CAN_MESSAGE)
        msg = can.Message(
            arbitration_id=msg.id, data=msg.data, is_extended_id=False
        )
        self.logger.info(f"CAN TX:" + str(msg))
        self.bus.send(msg, self.send_timeout)
        pass

    def can_recv(self) -> CAN_MESSAGE:
        message = self.bus.recv(self.receive_timeout)
        if (message is not None):
            message = CAN_MESSAGE(message.arbitration_id, message.data)
            self.logger.info(f"CAN RX:" + str(message))
        return message

    def disconnect(self):
        self.logger.info(f"Canbus closed!")
        self.bus.close()
        pass
