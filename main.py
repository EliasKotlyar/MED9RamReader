#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser

#from panda import Panda
from tp20 import TP20Transport
from kwp2000 import KWP2000Client, ECU_IDENTIFICATION_TYPE
import can

CHUNK_SIZE = 4
class SocketCan:
    def __init__(self):
        self.bus = can.interface.Bus(channel="can0", bustype="socketcan")
    def can_recv(self,timeout = 1):
        message = self.bus.recv(timeout) 
        #print(message)
        if message is None:
            print('Timeout occurred, no message.')
        ret = []
        ret.append((message.arbitration_id, 0, message.data, 0))
        return ret
        pass
    def can_send(self,addr, dat, timeout):
        msg = can.Message(
            arbitration_id=addr, data=dat, is_extended_id=False
        )
        #print(msg)
        self.bus.send(msg,timeout)
        pass
    
    
if __name__ == "__main__":


    socketcan = SocketCan()

    print("Connecting using KWP2000...")
    destId = 0x01;
    timeout = 1
    debug = False
    tp20 = TP20Transport(socketcan,destId, timeout, debug)
    kwp_client = KWP2000Client(tp20)

    print("Reading ecu identification & flash status")
    ident = kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.ECU_IDENT)
    print("ECU identification", ident)
    print(f"Part Number {ident[:10]}")
    

    status = kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.STATUS_FLASH)
    print("Flash status", status)
