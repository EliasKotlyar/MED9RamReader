from src.devices.vwdevice import VWDevice
from src.protocols.kwp2000 import SESSION_TYPE
from src.crypto.secaccess import MED91_READ_ACCESS
from src.crypto.secaccess import MED91_WRITE_ACCESS

class MED9:
    def __init__(self, logger=None):
        self.vwdevice = VWDevice(logger, 0x01)

    def connect(self):
        self.vwdevice.connect()


    def readMemory(self, memoryAdress, memorysize=1):
        secAccess = MED91_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        #data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
        data = self.vwdevice.readMemoryByDynamicIdentifier(memoryAdress, memorysize)
        return data
    def readMeasuringBlock(self, measuringBlockNr):
        data = self.vwdevice.readMeasuringBlock(measuringBlockNr)
        return data

    
    def readMemoryByUpload(self,memoryAdress : int, memorysize: int):
        secAccess = MED91_READ_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        self.vwdevice.changeSession(SESSION_TYPE.ENGINEERING_MODE)
        data = self.vwdevice.readMemoryRequestUpload(memoryAdress,memorysize)
        #print(f"Received Data: {data.hex()}")
        return data
    
    def writeMemoryByUpload(self,memoryAdress : int, memory: bytes):
        # Sequence taken from: "Corporate Group Requirement Specification For Programming Control Units with Keyword Protocol 2000 Transport Protocol 2.0.pdf"
        self.vwdevice.readEcuIdent()
        # Change Session:
        fBoot = self.vwdevice.changeSession(SESSION_TYPE.PROGRAMMING)
        print(fBoot)
        if(fBoot > 0):
            self.vwdevice.disconnect()
            self.vwdevice.reloadClient()
        # Sec Access:
        secAccess = MED91_WRITE_ACCESS()
        self.vwdevice.securityAccess(secAccess)
        # Send Download Request:
        data = self.vwdevice.writeMemoryRequestDownload(memoryAdress,memory)
        # Erase Flash:
        fRoutine = self.vwdevice.eraseFlash(memoryAdress,memory)
        if(fRoutine > 0):
            self.vwdevice.disconnect()
            self.vwdevice.reloadClient()
        result = self.vwdevice.requestEraseFlashResult(memoryAdress)
        self.vwdevice.transferData(memory)
        self.vwdevice.transferExit()

        self.vwdevice.requestCalculateChecksum()
        self.vwdevice.requestCalculateChecksumResult()







        # 
        #self.vwdevice.reloadClient()
        #self.vwdevice.securityAccess(secAccess)

        
        #print(f"Received Data: {data.hex()}")
        return data