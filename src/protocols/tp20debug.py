import struct

from src.protocols.kwp2000 import SERVICE_TYPE


class TP20Debug:
    def __init__(self, canbus):
        self.canbus = canbus
        pass

    def can_recv(self):
        while 1:
            message = self.canbus.can_recv(1)
            if message is not None:
                break
        return message

    def recv(self) -> bytes:
        """Receives multiple chunks of a response and combines
        them into a single string"""
        payload = b""
        while True:
            canMsg = self.can_recv()
            if canMsg.id==0x200:
                print("Request from Tester(setup):")
                print(canMsg)
            
            if canMsg.id==0x338:
                if(canMsg.data.hex() == "a3"):
                    continue
                if(len(canMsg.data) >= 4 ):
                    service_id = canMsg.data[3]
                    try:
                        service_desc = SERVICE_TYPE(service_id).name
                    except BaseException:
                        service_desc = "NON_STANDARD_SERVICE"
                    print("Service Type" + service_desc)    
                print("Request from Tester:")
                print(canMsg)
                
            if canMsg.id==0x300:
                if(canMsg.data.hex() == "a10f8aff4aff"):
                    continue

                #print("Response from ECU:")
                #print(canMsg)
                pass

        return data
