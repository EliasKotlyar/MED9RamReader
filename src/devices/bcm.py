from src.devices.vwdevice import VWDevice
class BCM:
    def __init__(self, debug=False):
        self.vwdevice = VWDevice(debug,0x20)
    def connect(self):
        self.vwdevice.connect()
        self.vwdevice.securityAccess2()
    def readMemory(self, memoryAdress, memorysize=1):
        return self.vwdevice.readMemoryRequestUpload(memoryAdress, memorysize)
    