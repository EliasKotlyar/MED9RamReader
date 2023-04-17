from src.devices.vwdevice import VWDevice
from src.protocols.kwp2000 import SESSION_TYPE
from src.crypto.secaccess import MED91_READ_ACCESS
from src.crypto.secaccess import MED91_WRITE_ACCESS

class MED9:
    def __init__(self, debug=False):
        self.vwdevice = VWDevice(debug, 0x01)

    def connect(self):
        self.vwdevice.connect()
        #sa2 = SA2()
        #self.vwdevice.securityAccess1(sa2)

        #self.vwdevice.changeSession(SESSION_TYPE.PROGRAMMING)

    def readMemory(self, memoryAdress, memorysize=1):
        secAccess = MED91_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        #data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
        data = self.vwdevice.readMemoryByDynamicIdentifier(memoryAdress, memorysize)
        return data
    
    
    def readByUpload(self):
        secAccess = MED91_READ_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        memoryAdress = 0x80000 
        memorysize=0x20000 
        data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
