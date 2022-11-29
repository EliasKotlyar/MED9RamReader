from tp20 import TP20Transport
from kwp2000 import KWP2000Client, ECU_IDENTIFICATION_TYPE ,DYNAMIC_DEFINITION_TYPE,DynamicSourceDefinition
import can
import struct
import time
CHUNK_SIZE = 4
from kwp2000 import ACCESS_TYPE, ROUTINE_CONTROL_TYPE, KWP2000Client, SESSION_TYPE, ECU_IDENTIFICATION_TYPE
from connections import canbus
from ccp import CcpClient, BYTE_ORDER

class MED9:
    def __init__(self, debug=False):
        self.bus = canbus.CANBUS()
        self.debug = debug
        self.tp20 = False
        self.kwp_client = False
        self.destId = 0x01
        self.timeout = 1


    def calculateSA2(self,seed):
        seedData = 0x5FBD5DBD
        #note: original java implementation used an "unsigned shift" for the rshift, but python numbers don't "have" a visible sign bit
        #and as such can be treated as pure u32.
        # (seed << 1) | (seed >> 31) is bitwise left rotate, by ORing the MSBit to the left-shift.
        for i in range(5): #5 shifts
            if ((seed & 0x80000000) == 0x80000000): # if the "to overflow" bit is set, xor with 'key'
                seed = (seedData) ^ ((seed << 1) | (seed >> 31)) & 0xffffffff # rotate left, xor, and clamp.
            else:
                seed = ((seed << 1) | (seed >> 31)) #rotate left only  
        return seed
    def connect(self):
        self.print("Connecting using KWP2000...")

        
        self.tp20 = TP20Transport(self.bus,self.destId, self.timeout, self.debug)
        self.kwp_client = KWP2000Client(self.tp20)
        
        self.print("Reading ecu identification & flash status")
        ident = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.ECU_IDENT)
        self.print("ECU identification", ident)
        self.print(f"Part Number {ident[:10]}")
        
        
        status = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.STATUS_FLASH)
        self.print("Flash status", status)
        
        #self.securityAccess2()
        self.securityAccess1()
        #self.changeSession(SESSION_TYPE.PROGRAMMING)
        #self.changeSession(SESSION_TYPE.ENGINEERING_MODE)
        
        
        #self.changeSession(SESSION_TYPE.ENGINEERING_MODE)

        #self.securityAccess()
        
        
        

    def securityAccess1(self):
        self.print("\nRequest seed")
        seed = self.kwp_client.security_access(ACCESS_TYPE.PROGRAMMING_REQUEST_SEED)
        self.print(f"seed: {seed.hex()}")
        seed_int = struct.unpack(">I", seed)[0]
        key_int = self.calculateSA2(seed_int)
        key = struct.pack(">I", key_int)
        self.print(f"key: {key.hex()}")
        
        self.print("\n Send key")
        self.kwp_client.security_access(ACCESS_TYPE.PROGRAMMING_SEND_KEY, key)
        self.print("\n Acess granted!")
        
    def securityAccess2(self):
        self.print("\nRequest seed")
        seed = self.kwp_client.security_access(ACCESS_TYPE.REQUEST_SEED)
        self.print(f"seed: {seed.hex()}")
        seed_int = struct.unpack(">I", seed)[0]
        key_int = seed_int + 0x00011170
        key = struct.pack(">I", key_int)
        self.print(f"key: {key.hex()}")
        self.print("\n Send key")
        self.kwp_client.security_access(ACCESS_TYPE.SEND_KEY, key)
        self.print("\n Acess granted!")
        
    def changeSession(self,session_type: SESSION_TYPE):
        #self.kwp_client.diagnostic_session_control(SESSION_TYPE.PROGRAMMING)
        self.kwp_client.diagnostic_session_control(session_type)
        #for i in range(10):
        #    time.sleep(1)
        #    self.print(f"\nReconnecting... {i}")
        #    try:
        #        tp20 = TP20Transport(self.bus,self.destId, self.timeout, self.debug)
        #        break
        #    except Exception as e:
        #        print(e)
        #self.tp20 = tp20
        #self.kwp_client = KWP2000Client(self.tp20)
    
    def keepChannelAlive(self):
        self.tp20.can_send(b"\xa3")
        self.tp20.can_recv()
        
    def print(self,*args):
        if self.debug:
            print(args)
    def readMemory(self,memoryAdress,memorysize=1):
        dyn = DynamicSourceDefinition(0,0,memorysize,memoryAdress)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF1 ,[dyn],4,1)
        data = self.kwp_client.read_data_by_identifier(0xF1)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER, 0xF1 ,[dyn],4,1)
        self.keepChannelAlive()
        return data
    def writeMemory(self,memoryAdress, value):
        memorysize=1
        dyn = DynamicSourceDefinition(0,0,memorysize,memoryAdress)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF2 ,[dyn],4,1)
        self.kwp_client.write_data_by_identifier(0xF2,value)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER, 0xF2 ,[dyn],4,1)
        self.keepChannelAlive()
        return data
    def readMemoryByCCP(self,memoryAdress,memorysize=1):
        self.print("Connecting using CCP...")
        client = CcpClient(self.bus, 0x7C3, 0x7C4, byte_order=BYTE_ORDER.LITTLE_ENDIAN)
        print(client.get_version())
        #client.connect(0x0)
        #client.set_memory_transfer_address(0, 0, memoryAdress)
        #client.upload(1)
    def readMemoryRequestUpload(self,memoryAdress,memorysize=1):
        self.kwp_client.request_upload(memoryAdress, memorysize)
    def sendRawCanBusMessage(self,addr, dat, timeout):
        self.bus.can_send(addr, dat, timeout)
    def writeRamCustomMethod(self,address,value):

        
        addressb1 = (address>>24) & 0xff
        addressb2 = (address>>16) & 0xff
        addressb3 = (address>>8) & 0xff
        addressb4 = address & 0xff
        
        valueb1 = (value>>24) & 0xff
        valueb2 = (value>>16) & 0xff
        valueb3 = (value>>8) & 0xff
        valueb4 = value & 0xff
        
        arr = [1, addressb2, addressb3, addressb4, valueb1, valueb2 , valueb3, valueb4 ]
        for i in arr:
            print(hex(i))
        self.sendRawCanBusMessage(0x539,arr,1)