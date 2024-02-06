from .datatypes import *
from .requests import *
from .constants import *
from .responses import *


class DataFormatIdentifier(bytearray):
    def __init__(self, comp_type: COMPRESSION_TYPE, enc_type: ENCRYPTION_TYPE):
        assert isinstance(comp_type, COMPRESSION_TYPE)
        assert isinstance(enc_type, ENCRYPTION_TYPE)
        bytes = Int8Bit(comp_type, enc_type)
        super().__init__(bytes)


class IDENT_9B(AbstractKwpRequest):
    def __init__(self):
        ret = READ_ECU_IDENTIFICATION(0x9B)
        super().__init__(ret.to_bytes())

    def get_positive_response(self, data: bytearray) -> KwpResponse:
        return IDENT_9B_Response(data)


class IDENT_9C(AbstractKwpRequest):
    def __init__(self):
        ret = READ_ECU_IDENTIFICATION(0x9C)
        super().__init__(ret.to_bytes())

    def get_positive_response(self, data: bytearray) -> KwpResponse:
        return IDENT_9C_Response(data)


class START_DIAGNOSTIC_SESSION_FLASH(AbstractKwpRequest):
    def __init__(self):
        ret = START_DIAGNOSTIC_SESSION(SESSION_TYPE.PROGRAMMING)
        super().__init__(ret.to_bytes())


class REQUEST_SEED_PROGRAMMING(AbstractKwpRequest):
    def __init__(self):
        payload = bytearray([
            ACCESS_TYPE.PROGRAMMING_REQUEST_SEED
        ])
        ret = SECURITY_ACCESS(payload)
        super().__init__(ret.to_bytes())

    def get_positive_response(self, data: bytearray) -> KwpResponse:
        return REQUEST_SEED_RESPONSE(data)


class SEND_KEY_PROGRAMMING(AbstractKwpRequest):
    def __init__(self, key: int):
        assert isinstance(key, int)
        payload = bytearray([
            ACCESS_TYPE.PROGRAMMING_SEND_KEY,
        ]) + Int32Bit(key)
        ret = SECURITY_ACCESS(payload)
        super().__init__(ret.to_bytes())


class REQUEST_DOWNLOAD_MED9(AbstractKwpRequest):
    def __init__(self, memory_address: int, uncompressed_size: int):
        assert isinstance(memory_address, int)
        assert isinstance(uncompressed_size, int)

        compression_type = COMPRESSION_TYPE.COMPRESSION_1
        encryption_type = ENCRYPTION_TYPE.ENCRYPTION_1
        identifier = DataFormatIdentifier(compression_type, encryption_type)
        memory_address = Int24Bit(memory_address)
        uncompressed_size = Int24Bit(uncompressed_size)
        payload = memory_address + identifier + uncompressed_size
        ret = REQUEST_DOWNLOAD(payload)
        super().__init__(ret.to_bytes())


class START_ROUTINE_ERASE_FLASH(AbstractKwpRequest):
    def __init__(self, start_addr: int, end_address: int, ftc: FlashToolCode):
        assert isinstance(start_addr, int)
        assert isinstance(end_address, int)
        assert isinstance(ftc, FlashToolCode)
        start_addr = Int24Bit(start_addr)
        end_address = Int24Bit(end_address)
        payload = start_addr + end_address + ftc
        ret = START_ROUTINE_BY_LOCAL_IDENTIFIER(ROUTINE_CONTROL_TYPE.ERASE_FLASH, bytearray(payload))
        super().__init__(ret.to_bytes())


class START_ROUTINE_CHECKSUM(AbstractKwpRequest):
    def __init__(self, start_addr: int, end_address: int, checksum: int):
        assert isinstance(start_addr, int)
        assert isinstance(end_address, int)
        assert isinstance(checksum, int)
        start_addr = Int24Bit(start_addr)
        end_address = Int24Bit(end_address)
        checksum = Int16Bit(checksum)
        payload = start_addr + end_address + checksum.toBytes
        ret = START_ROUTINE_BY_LOCAL_IDENTIFIER(ROUTINE_CONTROL_TYPE.CALCULATE_FLASH_CHECKSUM, payload)
        super().__init__(ret.to_bytes())


class GET_RESULT_ROUTINE_ERASE_FLASH(AbstractKwpRequest):
    def __init__(self):
        ret = REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER(ROUTINE_CONTROL_TYPE.ERASE_FLASH, bytearray([]))
        super().__init__(ret.to_bytes())


class GET_RESULT_ROUTINE_CHECKSUM(AbstractKwpRequest):
    def __init__(self):
        ret = REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER(ROUTINE_CONTROL_TYPE.CALCULATE_FLASH_CHECKSUM, bytearray([]))
        super().__init__(ret.to_bytes())
