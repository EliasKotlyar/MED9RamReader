from src.protocols.tp20 import TP20Transport
from src.protocols.kwp2000 import DYNAMIC_DEFINITION_TYPE, \
    DynamicSourceDefinition
import struct
import time

CHUNK_SIZE = 4
from src.protocols.kwp2000 import ACCESS_TYPE, KWP2000Client, SESSION_TYPE, \
    ECU_IDENTIFICATION_TYPE, COMPRESSION_TYPE, ENCRYPTION_TYPE
from src.connections import canbus
from src.protocols.ccp import CcpClient, BYTE_ORDER
from src.crypto.secaccess import SecurityAccessInterface
from src.protocols.logger import Logger
from src.protocols.kwp2000.measuringblocks import MeasuringBlockGroup


class VWDevice:
    def __init__(self, logger: Logger = None, destId=1):
        self.bus = canbus.CANBUS()
        self.logger = logger
        self.tp20 = False
        self.kwp_client = False
        self.destId = destId
        self.timeout = 30

    def connect(self):
        self.print("Connecting using KWP2000...")
        self.tp20 = TP20Transport(self.bus, self.destId, self.timeout, self.logger)
        self.kwp_client = KWP2000Client(self.tp20, self.logger)

    def readEcuIdent(self):
        self.print("Reading ecu identification & flash status")
        ident = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.ECU_IDENT)
        self.print("ECU identification", ident)
        self.print(f"Part Number {ident[:10]}")

        status = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.STATUS_FLASH)
        self.print("Flash status", status)

        status = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.HW_NUMBER)
        self.print("VehicleHWNumber", status)

        status = self.kwp_client.read_ecu_identifcation(ECU_IDENTIFICATION_TYPE.HW_NUMBER2)
        self.print("VehicleHWNumber2", status)

    def securityAccess(self, secInterface: SecurityAccessInterface):
        if (secInterface.getAccessType() == secInterface.PROGRAMMING):

            secAccess1 = ACCESS_TYPE.PROGRAMMING_REQUEST_SEED
            secAccess2 = ACCESS_TYPE.PROGRAMMING_SEND_KEY
            pass
        elif (secInterface.getAccessType() == secInterface.NORMAL):
            secAccess1 = ACCESS_TYPE.REQUEST_SEED_PROGRAMMING
            secAccess2 = ACCESS_TYPE.SEND_KEY_PROGRAMMING
            pass

        self.print("\nRequest seed")
        seed = self.kwp_client.security_access(secAccess1)
        self.print(f"seed: {seed.hex()}")
        seed_int = struct.unpack(">I", seed)[0]
        key_int = secInterface.calculate(seed_int)
        key = struct.pack(">I", key_int)
        self.print(f"key: {key.hex()}")

        self.print("\n Send key")
        self.kwp_client.security_access(secAccess2, key)
        self.print("\n Acess granted!")

    def changeSession(self, session_type: SESSION_TYPE):
        # self.kwp_client.diagnostic_session_control(SESSION_TYPE.PROGRAMMING)
        return self.kwp_client.diagnostic_session_control(session_type)

    def reloadClient(self):
        for i in range(10):
            time.sleep(1)
            self.print(f"\nReconnecting... {i}")
            try:
                tp20 = TP20Transport(self.bus, self.destId, self.timeout, self.logger)
                break
            except Exception as e:
                print(e)
        self.tp20 = tp20
        self.kwp_client = KWP2000Client(self.tp20, self.logger)
        self.keepChannelAlive()
        self.print("\n Session changed!")

    def keepChannelAlive(self):
        self.tp20.can_send(b"\xa3")
        self.tp20.can_recv()

    def print(self, *args):
        if self.logger:
            self.logger.log(args)

    def readMemoryByAddress(self, memoryAdress, memorysize=1):
        self.keepChannelAlive()
        data = self.kwp_client.read_memory_by_address(memory_address=memoryAdress, memory_size=memorysize)

        return data

    def dynamicallyDefineIdentifier(self, identifier: int, memoryAddress: int, memorySize: int):
        dyn = DynamicSourceDefinition(0, 0, memorySize, memoryAddress)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, identifier,
                                                           [dyn], 4, 1)

    def readMemoryByDynamicIdentifier(self, memoryAdress, memorysize=1):
        dyn = DynamicSourceDefinition(0, 0, memorysize, memoryAdress)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF1,
                                                           [dyn], 4, 1)
        data = self.kwp_client.read_data_by_identifier(0xF1)
        self.kwp_client.dynamically_define_data_identifier(
            DYNAMIC_DEFINITION_TYPE.CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER, 0xF1, [dyn], 4, 1)
        self.keepChannelAlive()
        return data

    def writeMemoryByDynamicIdentifier(self, memoryAdress, value):
        memorysize = 1
        dyn = DynamicSourceDefinition(0, 0, memorysize, memoryAdress)
        self.kwp_client.dynamically_define_data_identifier(DYNAMIC_DEFINITION_TYPE.DEFINE_BY_MEMORY_ADDRESS, 0xF2,
                                                           [dyn], 4, 1)
        self.kwp_client.write_data_by_identifier(0xF2, value)
        self.kwp_client.dynamically_define_data_identifier(
            DYNAMIC_DEFINITION_TYPE.CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER, 0xF2, [dyn], 4, 1)
        self.keepChannelAlive()
        return data

    def readMemoryByCCP(self, memoryAdress, memorysize=1):
        self.print("Connecting using CCP...")
        client = CcpClient(self.bus, 0x7C3, 0x7C4, byte_order=BYTE_ORDER.LITTLE_ENDIAN)
        print(client.get_version())
        # client.connect(0x0)
        # client.set_memory_transfer_address(0, 0, memoryAdress)
        # client.upload(1)

    def readMemoryRequestUpload(self, memoryAdress, memorysize=1):
        self.kwp_client.request_upload(memoryAdress, memorysize)
        self.keepChannelAlive()
        data = self.kwp_client.transfer_data(data=None)
        self.kwp_client.request_transfer_exit()
        return data

    def writeMemoryRequestDownload(self, memoryAdress, memory: bytes):

        memorySize = len(memory)
        self.kwp_client.request_download(memoryAdress, memorySize, COMPRESSION_TYPE.COMPRESSION_1,
                                         ENCRYPTION_TYPE.ENCRYPTION_1)
        self.keepChannelAlive()
        data = self.kwp_client.transfer_data(memory)
        self.kwp_client.request_transfer_exit()
        return data

    def readMeasuringBlock(self, measuringBlockNr):
        data = self.kwp_client.read_data_by_identifier(measuringBlockNr)
        group = MeasuringBlockGroup(data)
        return group

    def sendRawCanBusMessage(self, addr, dat, timeout):
        self.bus.can_send(addr, dat, timeout)

    def writeRamCustomMethod(self, address, value):

        addressb1 = (address >> 24) & 0xff
        addressb2 = (address >> 16) & 0xff
        addressb3 = (address >> 8) & 0xff
        addressb4 = address & 0xff

        valueb1 = (value >> 24) & 0xff
        valueb2 = (value >> 16) & 0xff
        valueb3 = (value >> 8) & 0xff
        valueb4 = value & 0xff

        arr = [1, addressb2, addressb3, addressb4, valueb1, valueb2, valueb3, valueb4]
        for i in arr:
            print(hex(i))
        self.sendRawCanBusMessage(0x539, arr, 1)

    def disconnect(self):
        if self.kwp_client:
            self.kwp_client.stop_communication()
        self.bus.disconnect()
        pass

    def writeMemoryByAddress(self, memoryAdress: int, memory: bytes):
        self.keepChannelAlive()
        data = self.kwp_client.write_memory_by_address(memoryAdress, memory)

        return data
