import logging

from src.misc.dump_file import read_dump_file
from src.protocols.flasher.flasher import FlashProgrammer


dump = read_dump_file("dump.bin")
f = FlashProgrammer()
logging.getLogger("kwp").setLevel(logging.INFO)
logging.getLogger("med9flasher").setLevel(logging.INFO)
#logging.getLogger("tp20").setLevel(logging.INFO)
f.flash_file(dump)
