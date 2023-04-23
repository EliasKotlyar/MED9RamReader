from src.devices.vwdevice import VWDevice
from src.protocols.kwp2000 import SESSION_TYPE
from src.crypto.secaccess import MED91_READ_ACCESS
from src.crypto.secaccess import MED91_WRITE_ACCESS

class MED9:
    def __init__(self, logger=None):
        self.vwdevice = VWDevice(logger, 0x01)

    def connect(self):
        self.vwdevice.connect()
        self.vwdevice.readEcuIdent()

    def readMemory(self, memoryAdress, memorysize=1):
        secAccess = MED91_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        #data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
        data = self.vwdevice.readMemoryByDynamicIdentifier(memoryAdress, memorysize)
        return data
    
    
    def readMemoryByUpload(self,memoryAdress : int, memorysize: int):
        secAccess = MED91_READ_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        self.vwdevice.changeSession(SESSION_TYPE.ENGINEERING_MODE)
        data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
        #print(f"Received Data: {data.hex()}")
        return data
    
    def writeMemoryByUpload(self,memoryAdress : int, memory: bytes):
        secAccess = MED91_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        #self.vwdevice.changeSession(SESSION_TYPE.PROGRAMMING)
        #self.vwdevice.reloadClient()
        #self.vwdevice.securityAccess(secAccess)

        data = self.vwdevice.writeMemoryRequestDownload(memoryAdress,memory)
        #print(f"Received Data: {data.hex()}")
        return data