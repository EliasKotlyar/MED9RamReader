from src.devices.vwdevice import VWDevice


class MED9:
    def __init__(self, debug=False):
        self.vwdevice = VWDevice(debug, 0x01)

    def connect(self):
        self.vwdevice.connect()
        self.vwdevice.securityAccess1()

    def readMemory(self, memoryAdress, memorysize=1):
        self.vwdevice.readMemory(memoryAdress, memorysize)
        pass
