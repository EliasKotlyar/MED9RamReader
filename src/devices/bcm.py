from src.devices.vwdevice import VWDevice
from src.crypto.secaccess import BCM_WRITE_ACCESS
from src.crypto.secaccess import BCM_READ_ACCESS
from src.protocols.kwp2000 import SESSION_TYPE
class BCM:
    def __init__(self, debug=False):
        self.vwdevice = VWDevice(debug,0x20)
    def connect(self):
        self.vwdevice.connect()

    def readMemory(self, memoryAdress, memorysize=1):
        #self.vwdevice.changeSession(SESSION_TYPE.ENGINEERING_MODE)

        #secAccess = BCM_READ_ACCESS()
        #self.vwdevice.securityAccess(secAccess)
        return self.vwdevice.readMemoryRequestUpload(memoryAdress, memorysize)
    
    def writeMemory(self):
        self.vwdevice.changeSession(SESSION_TYPE.PROGRAMMING)
        secAccess = BCM_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)