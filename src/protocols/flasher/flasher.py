# Assuming the classes are already defined as described in the previous response
import logging
import time

from src.connections import canbus
from src.crypto.secaccess import MED91_WRITE_ACCESS
from src.crypto.xor import xor_encrypt, MED9_XOR_KEY
from src.misc.binarydump import BinaryDump
from src.protocols.flasher.flash_blocks import med9_flashblocks, FlashBlock
from src.protocols.kwp2000.extended_requests import *
from src.protocols.kwp2000client import KWP2000Client, KWP_Exception
from src.protocols.tp20client import TP20Transport


class FlashProgrammer:
    def __init__(self):
        self.initlogger()
        self.logger = logging.getLogger("med9flasher")
        self.bus = canbus.CANBUS()
        self.destId = 1
        self.timeout = 50
        self.tp20 = None
        self.ftc = "MED9FL"
        self.reloadClient()

    def check_bootloader(self):
        ret = False
        response = self.kwp.send(READ_ECU_IDENTIFICATION(0x81), False)
        if response.data.hex() == "5a810591016c01099b6c640404026f65039c04ff":
            ret = True
        return ret

    def perform_auth(self):
        response: REQUEST_SEED_RESPONSE = self.kwp.send(REQUEST_SEED_PROGRAMMING())
        self.logger.debug(response)
        self.logger.debug("Seed: " + str(response.seed))
        med9write = MED91_WRITE_ACCESS()
        key = med9write.calculate(response.seed)
        self.logger.debug("Key: " + str(key))
        response: KwpResponse = self.kwp.send(SEND_KEY_PROGRAMMING(key))
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

    def erase_flash(self, block: FlashBlock):
        self.logger.info(f"Erasing Flash!")
        end_address = block.addr + block.size - 1
        cmd = START_ROUTINE_ERASE_FLASH(block.addr, end_address, FlashToolCode(self.ftc))
        self.logger.debug(str(cmd))
        response = self.kwp.send(cmd)
        self.logger.info(str(response))
        response = self.kwp.send(GET_RESULT_ROUTINE_ERASE_FLASH())
        self.logger.debug(str(response))
        self.logger.info(f"Erase Flash sucesful!")

    def transferData(self, block: FlashBlock):
        self.logger.info(f"Sending Data!")
        chunk_size = 250
        data = block.payload
        num_chunks = (len(data) + chunk_size - 1) // chunk_size  # Calculate the number of chunks needed
        for i in range(num_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(data))
            chunk = data[start:end]
            self.kwp.send(TRANSFER_DATA(bytearray(chunk)))
        self.logger.info(f"Sending End!")

    def flash_block(self, block: FlashBlock):
        block_addr = block.addr
        block_size = block.size
        checksum = block.crc

        self.logger.info(f"Trying to write block {block_addr} with Size {block_size} and CHKSUM {checksum}")
        self.logger.info(f"FTC: {self.ftc}")

        self.logger.info(f"Sending Request Download!")
        response = self.kwp.send(REQUEST_DOWNLOAD_MED9(block_addr, block_size))
        self.logger.debug(str(response))
        self.logger.info(f"Sending Request sucessful!")
        self.erase_flash(block)
        self.transferData(block)

        self.kwp.send(REQUEST_TRANSFER_EXIT())

        self.logger.info(f"Sending Checksum:")
        self.kwp.send(START_ROUTINE_CHECKSUM(block_addr, end_address, checksum))
        self.kwp.send(GET_RESULT_ROUTINE_CHECKSUM())
        self.logger.info(f"Sending Checksum!")

    def flash_file(self, file: BinaryDump):
        med9_blocks = med9_flashblocks
        self.logger.info(f"Filling Block ")
        for block in med9_blocks:
            assert isinstance(block, FlashBlock)
            payload = file.get_part(block.addr, block.size).get_bytes()
            block.addPayload(payload)
            block.buildCrc()
            block.encrypt()
        # Boot into Bootloader:
        self.boot_into_bootloader()
        # Perform auth on Bootloader:
        self.logger.info(f"Performing Auth(Bootloader)")
        self.perform_auth()
        self.logger.info(f"Auth sucesful!")
        for block in med9_blocks:
            self.flash_block(block)

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
        self.kwp.send(REQUEST_RESET_ECU())
        pass

    def initlogger(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        loggers = ["tp20", "kwp", "med9flasher"]
        for logger in loggers:
            logger = logging.getLogger(logger)
            logger.setLevel(logging.ERROR)
            logger.addHandler(console_handler)
