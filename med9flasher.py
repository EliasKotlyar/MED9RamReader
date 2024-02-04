# Assuming the classes are already defined as described in the previous response
from src.protocols.kwp2000.extended_requests import IDENT_9B

class FlashProgrammer:
    def boot_into_bootloader(self):
        response = kwp.send(IDENT_9B())
        print(response)
        response = kwp.send(IDENT_9C())
        print(response)
        response = kwp.send(START_DIAGNOSTIC_SESSION_FLASH())
        print(response)
        response = kwp.send(REQUEST_SEED())
        print(response)
        key = calculate(response.seed)
        response = kwp.send(SEND_KEY(key))
        print(response)
        sleep(response.boot_f)
        response = kwp.send(REQUEST_SEED())
        print(response)
        key = calculate(response.seed)
        response = kwp.send(SEND_KEY(key))
        print(response)
    def flash_block(self):
        response = kwp.send(RequestDownload(key))
        print(response)
        response = kwp.send(StartRoutineByLocalIdentifier0xC4())
        print(response)
        response = kwp.send(RequestRoutineResultsByLocalIdentifier0xC4())
        print(response)
        response = kwp.send(TransferData())
        print(response)
        response = kwp.send(TransferExit())
        print(response)
        response = kwp.send(StartRoutineByLocalIdentifier0xC5())
        print(response)
        response = kwp.send(RequestRoutineResultsByLocalIdentifier0xC5())
        print(response)






