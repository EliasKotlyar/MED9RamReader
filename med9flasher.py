# Assuming the classes are already defined as described in the previous response
import logging
import time

from src.connections import canbus
from src.crypto.secaccess import MED91_WRITE_ACCESS
from src.protocols.kwp2000.extended_requests import *
from src.protocols.kwp2000client import KWP2000Client, KWP_Error
from src.protocols.tp20client import TP20Transport


class FlashProgrammer:
    def __init__(self):
        self.logger = logging.getLogger("med9flasher")
        self.bus = canbus.CANBUS()
        self.destId = 1
        self.timeout = 50
        self.reloadClient()

    def check_bootloader(self):
        response = self.kwp.send(TESTER_PRESENT())
        #rint(response)

    def perform_auth(self):
        response = self.kwp.send(REQUEST_SEED())
        assert response, REQUEST_SEED_RESPONSE
        med9write = MED91_WRITE_ACCESS()
        key = med9write.calculate(response.seed)
        response = self.kwp.send(SEND_KEY(key))

    def boot_into_bootloader(self):
        response: IDENT_9B_Response = self.kwp.send(IDENT_9B())
        self.logger.info(f"Got Ident 9B. VW Part number {response.vw_part_nr}")
        self.logger.debug(str(response))
        response: IDENT_9C_Response = self.kwp.send(IDENT_9C())
        self.logger.info(f"Got Ident 9C. Flash Status {response.preprogramming_status}")
        self.logger.debug(str(response))

        try:
            self.logger.info(f"Trying to switch to Diag-Session...")
            self.kwp.send(START_DIAGNOSTIC_SESSION_FLASH())
            raise KWP_Error(0, "")
        except KWP_Error as e:
            if (e.code != 0x7F):
                raise e
        self.logger.info(f"Failed to switch session. This is intended")
        self.logger.info(f"Performing Auth")
        self.perform_auth()
        self.logger.info(f"Auth sucesful!")
        self.logger.info(f"Trying to switch to Diag-Session...")
        response: KwpResponse = self.kwp.send(START_DIAGNOSTIC_SESSION_FLASH())
        self.logger.debug(response)
        self.logger.info(f"Switched to Diag-Session!")
        self.logger.info(f"Reloading TP20 Session..")
        self.reloadClient()
        self.logger.info(f"Reload sucesful!")
        self.logger.info(f"Performing Auth(Bootloader)")
        self.perform_auth()
        self.logger.info(f"Auth sucesful!")
        self.logger.info(f"Check if bootet into bootloader...")
        self.check_bootloader()
        self.logger.info(f"Bootloader boot sucesful!")

    def flash_block(self):
        self.kwp.send(REQUEST_DOWNLOAD_MED9())

        self.kwp.send(START_ROUTINE_ERASE_FLASH())

        self.kwp.send(GET_RESULT_ROUTINE_ERASE_FLASH())

        self.kwp.send(TRANSFER_DATA())

        self.kwp.send(REQUEST_TRANSFER_EXIT())

        self.kwp.send(START_ROUTINE_CHECKSUM())

        self.kwp.send(GET_RESULT_ROUTINE_CHECKSUM())

    def reloadClient(self):
        for i in range(10):
            try:
                self.tp20 = TP20Transport(self.bus, self.destId, self.timeout)
                break
            except Exception as e:
                self.logger.info(e)
            time.sleep(1)
            self.logger.info(f"\nReconnecting... {i}")
        self.kwp = KWP2000Client(self.tp20)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
loggers = ["tp20", "kwp", "med9flasher"]
for logger in loggers:
    logger = logging.getLogger(logger)
    logger.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

# logging.getLogger("kwp").setLevel(logging.INFO)
logging.getLogger("med9flasher").setLevel(logging.INFO)

f = FlashProgrammer()
f.boot_into_bootloader()
# f.check_bootloader()
