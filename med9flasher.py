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
        self.tp20 = None
        self.reloadClient()

    def check_bootloader(self):
        ret = False
        try:
            response = self.kwp.send(READ_ECU_IDENTIFICATION(0x81))
            if response.data.hex() == "5a810591016c01099b6c640404026f65039c04ff":
                ret = True
        except KWP_Error as e:
            pass
        return ret

    def perform_auth(self):
        response: REQUEST_SEED_RESPONSE = self.kwp.send(REQUEST_SEED())
        self.logger.debug(response)
        self.logger.debug("Seed: " + str(response.seed))
        med9write = MED91_WRITE_ACCESS()
        key = med9write.calculate(response.seed)
        self.logger.debug("Key: " + str(key))
        response: KwpResponse = self.kwp.send(SEND_KEY(key))
        self.logger.debug(response)

    def boot_into_bootloader(self):
        self.logger.info(f"Checking if already in Bootloader...")
        if self.check_bootloader():
            self.logger.info(f"Is already in Bootloader.")
            return
        self.logger.info(f"ECU is not in Bootloader. Booting into Bootloader")
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
        self.logger.info(response)
        self.logger.info(f"Switched to Diag-Session!")
        self.logger.info(f"Waiting until TP20 Disconnects!")
        self.tp20.wait_until_disconnect()
        self.logger.info(f"Disconnect Sucessful!")
        self.logger.info(f"Reloading TP20 Session..")
        self.reloadClient()
        self.logger.info(f"Reload sucesful!")
        self.logger.info(f"Check if booted into bootloader...")
        if self.check_bootloader() == False:
            self.logger.info(f"Coult not boot into Bootloader")
            raise Exception('Coult not boot into Bootloader.')
        self.logger.info(f"Bootloader boot sucesful!")

    def flash_block(self):
        self.logger.info(f"Performing Auth(Bootloader)")
        self.perform_auth()
        self.logger.info(f"Auth sucesful!")
        block_addr = 0x1C0000
        block_size = 0x30000
        end_address = block_addr + block_size
        ftc = bytearray([0x1, 0x2, 0x3, 0x4, 0x5, 0x6])

        # self.kwp.send(REQUEST_TRANSFER_EXIT())

        self.logger.info(f"Sending Request Download!")
        #response = self.kwp.send(REQUEST_DOWNLOAD_MED9(block_addr, block_size))
        #self.logger.debug(str(response))
        self.logger.info(f"Sending Request sucessful!")

        self.logger.info(f"Erasing Flash!")

        #response = self.kwp.send(START_ROUTINE_ERASE_FLASH(block_addr, end_address, ftc))
        #self.logger.debug(str(response))
        self.logger.info(f"Erase Flash sucesful!")

        # self.logger.info(f"Sending Request Download!")
        #self.kwp.send(GET_RESULT_ROUTINE_ERASE_FLASH())

        self.kwp.send(TRANSFER_DATA(bytearray([0xFF])))

        self.kwp.send(REQUEST_TRANSFER_EXIT())
        checksum = 0
        self.kwp.send(START_ROUTINE_CHECKSUM(block_addr, end_address, checksum))

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

    def reset(self):
        #self.kwp.send(REQUEST_RESET_ECU())
        pass


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
loggers = ["tp20", "kwp", "med9flasher"]
for logger in loggers:
    logger = logging.getLogger(logger)
    logger.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

logging.getLogger("kwp").setLevel(logging.INFO)
logging.getLogger("med9flasher").setLevel(logging.INFO)
# logging.getLogger("tp20").setLevel(logging.INFO)

f = FlashProgrammer()

f.boot_into_bootloader()
f.flash_block()


