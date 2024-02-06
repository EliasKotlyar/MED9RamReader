from __future__ import annotations

import io

from src.crypto.crc32 import *
from src.crypto.lzss import compress
from src.crypto.xor import *


class FlashBlock:
    def __init__(self, addr: int, size: int):
        self.size = size
        self.addr = addr
        self.crc = 1234
        self.payload = bytearray()

    def addPayload(self, payload: bytearray):
        assert isinstance(payload, bytearray)
        self.payload = payload
        pass

    def buildCrc(self):
        self.crc = crc_32_fast(self.payload)
        pass

    def encrypt(self):
        binary_stream = io.BytesIO()
        compress(self.payload, binary_stream)
        binary_content = binary_stream.getvalue()
        self.payload = binary_content
        self.payload = xor_encrypt(self.payload, MED9_XOR_KEY)
        pass


med9_flashblocks = [
    FlashBlock(0x20000, 0x60000),
    FlashBlock(0xA0000, 0x120000),
    FlashBlock(0x1F0000, 0x10000),
    FlashBlock(0x80000, 0x20000),
    FlashBlock(0x1C0000, 0x30000)
]
