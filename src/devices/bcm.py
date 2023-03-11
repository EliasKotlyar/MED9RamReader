from src.devices.vwdevice import VWDevice
class BCM:
    def __init__(self, debug=False):
        self.vwdevice = VWDevice(debug,0x09)
    def connect(self):
        self.vwdevice.connect()
    def readMemory(self):
        pass