# Assuming the classes are already defined as described in the previous response
from src.connections import canbus
from src.crypto.secaccess import MED91_WRITE_ACCESS
from src.protocols.kwp2000.extended_requests import *
from src.protocols.kwp2000client import KWP2000Client
from src.protocols.tp20 import TP20Transport


class FlashProgrammer:
    def __init__(self):
        self.bus = canbus.CANBUS()
        self.destId = 1
        self.timeout = 30
        self.tp20 = TP20Transport(self.bus, self.destId, self.timeout)
        self.kwp = KWP2000Client(self.tp20)

    def boot_into_bootloader(self):
        response = self.kwp.send(IDENT_9B())
        # print(response)
        # return
        response = self.kwp.send(IDENT_9C())
        # print(response)
        # return

        # self.kwp.send(START_DIAGNOSTIC_SESSION_FLASH())
        # return

        response = self.kwp.send(REQUEST_SEED())
        assert response, REQUEST_SEED_RESPONSE
        print(response)
        med9write = MED91_WRITE_ACCESS()
        key = med9write.calculate(response.seed)
        response = self.kwp.send(SEND_KEY(key))
        print(response)

        # sleep(response.boot_f)
        # self.kwp.send(REQUEST_SEED())

        # key = calculate(response.seed)
        # self.kwp.send(SEND_KEY(key))

    def flash_block(self):
        self.kwp.send(RequestDownload(key))

        self.kwp.send(StartRoutineByLocalIdentifier0xC4())

        self.kwp.send(RequestRoutineResultsByLocalIdentifier0xC4())

        self.kwp.send(TransferData())

        self.kwp.send(TransferExit())

        self.kwp.send(StartRoutineByLocalIdentifier0xC5())

        self.kwp.send(RequestRoutineResultsByLocalIdentifier0xC5())

    def calculate(self, seed):
        pass


f = FlashProgrammer()
f.boot_into_bootloader()
