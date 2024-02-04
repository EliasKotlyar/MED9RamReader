from .requests import *
from .constants import *
from .responses import *


class FlashToolCode:
    def __init__(self, value: str):
        self.bytes = 0
        pass

    def toBytes(self):
        return bytearray(self.bytes)


class Int_4Bytes:
    def __init__(self, value: int):
        self.bytes = BitArray(uint=value, length=32).tobytes()
        pass

    def toBytes(self):
        return bytearray(self.bytes)


class Int_3Bytes:
    def __init__(self, value: int):
        self.bytes = 0
        pass

    def toBytes(self):
        return self.bytes


class DataFormatIdentifier:
    def __init__(self, comp_type: COMPRESSION_TYPE, enc_type: ENCRYPTION_TYPE):
        self.byte = 0
        pass

    def toByte(self):
        return self.byte


class IDENT_9B(AbstractKwpRequest):
    def __init__(self):
        ret = READ_ECU_IDENTIFICATION(0x9B)
        super().__init__(ret.to_bytes())

    def get_response(self, data: bytearray) -> KwpResponse:
        return IDENT_9B_Response(data)


class IDENT_9C(AbstractKwpRequest):
    def __init__(self):
        ret = READ_ECU_IDENTIFICATION(0x9C)
        super().__init__(ret.to_bytes())

    def get_response(self, data: bytearray) -> KwpResponse:
        return IDENT_9C_Response(data)


class START_DIAGNOSTIC_SESSION_FLASH(AbstractKwpRequest):
    def __init__(self):
        ret = START_DIAGNOSTIC_SESSION(SESSION_TYPE.PROGRAMMING)
        super().__init__(ret.to_bytes())


class REQUEST_SEED(AbstractKwpRequest):
    def __init__(self):
        payload = bytearray([
            ACCESS_TYPE.REQUEST_SEED
        ])
        ret = SECURITY_ACCESS(payload)
        super().__init__(ret.to_bytes())

    def get_response(self, data: bytearray) -> KwpResponse:
        return REQUEST_SEED_RESPONSE(data)


class SEND_KEY(AbstractKwpRequest):
    def __init__(self, key: int):
        assert key, int
        payload = bytearray([
            ACCESS_TYPE.SEND_KEY,
        ]) + Int_4Bytes(key).toBytes()
        ret = SECURITY_ACCESS(payload)
        super().__init__(ret.to_bytes())


class REQUEST_DOWNLOAD_MED9(AbstractKwpRequest):
    def __init__(self, memory_address: int, uncompressed_size: int):
        compression_type = COMPRESSION_TYPE.COMPRESSION_1
        encryption_type = ENCRYPTION_TYPE.UNENCRYPTED
        identifier = DataFormatIdentifier(compression_type, encryption_type)
        memory_address = Int_4Bytes(memory_address)
        uncompressed_size = Int_4Bytes(uncompressed_size)
        payload = bytearray([
            identifier.toByte(), memory_address.toBytes(), uncompressed_size.toBytes()
        ])
        ret = REQUEST_DOWNLOAD(payload)
        super().__init__(ret.to_bytes())
