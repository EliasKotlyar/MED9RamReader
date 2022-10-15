#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser

#from panda import Panda
from tp20 import TP20Transport
from kwp2000 import KWP2000Client, ECU_IDENTIFICATION_TYPE ,DYNAMIC_DEFINITION_TYPE,DynamicSourceDefinition
import can
import struct
from sa2 import SA2

CHUNK_SIZE = 4
from kwp2000 import ACCESS_TYPE, ROUTINE_CONTROL_TYPE, KWP2000Client, SESSION_TYPE, ECU_IDENTIFICATION_TYPE
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
    print()

    socketcan = SocketCan()

    print("Connecting using KWP2000...")
    destId = 0x01;
    timeout = 1
    debug = True
    tp20 = TP20Transport(socketcan,destId, timeout, debug)
    kwp_client = KWP2000Client(tp20)

    print("Reading ecu identification & flash status")
    ident = kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.ECU_IDENT)
    print("ECU identification", ident)
    print(f"Part Number {ident[:10]}")
    

    status = kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.STATUS_FLASH)
    print("Flash status", status)
    
    print("\nRequest seed")
    seed = kwp_client.security_access(ACCESS_TYPE.PROGRAMMING_REQUEST_SEED)
    print(f"seed: {seed.hex()}")
    
    seed_int = struct.unpack(">I", seed)[0]
    key_int = SA2.calculateSA2(seed_int)
    key = struct.pack(">I", key_int)
    print(f"key: {key.hex()}")

    print("\n Send key")
    kwp_client.security_access(ACCESS_TYPE.PROGRAMMING_SEND_KEY, key)
    print("\n Acess granted!")
    #kwp_client.read_data_by_identifier(0xF199)
    dyn = DynamicSourceDefinition(0,0,4,0x804334)
    print(dyn)
    
    kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF1 ,[dyn],4,1)
    