from .constants import SERVICE_TYPE
from .responses import KwpResponse


class AbstractKwpRequest:
    def __init__(self, data: bytearray):
        self.data = data

    def to_bytes(self) -> bytearray:
        return self.data

    def get_response(self, data: bytearray) -> KwpResponse:
        return KwpResponse(data)

    def __str__(self):
        return str(self.__class__.__name__) + " " + self.data.hex()


class READ_ECU_IDENTIFICATION(AbstractKwpRequest):
    def __init__(self, local_identifier: int):
        assert local_identifier, int
        data = bytearray([SERVICE_TYPE.READ_ECU_IDENTIFICATION, local_identifier])
        super().__init__(data)


class START_DIAGNOSTIC_SESSION(AbstractKwpRequest):
    def __init__(self, session_type: int):
        assert session_type, int
        data = bytearray([SERVICE_TYPE.START_DIAGNOSTIC_SESSION, session_type])
        super().__init__(data)


class SECURITY_ACCESS(AbstractKwpRequest):
    def __init__(self, data: bytearray):
        assert data, bytearray
        data = bytearray([SERVICE_TYPE.SECURITY_ACCESS]) + data
        super().__init__(data)


class REQUEST_DOWNLOAD(AbstractKwpRequest):
    def __init__(self, data: bytearray):
        assert data, bytearray
        data = bytearray([SERVICE_TYPE.REQUEST_DOWNLOAD]) + data
        super().__init__(data)


class START_ROUTINE_BY_LOCAL_IDENTIFIER(AbstractKwpRequest):
    def __init__(self, local_identifier: int, data: bytearray):
        assert data, bytearray
        data = bytearray([SERVICE_TYPE.START_ROUTINE_BY_LOCAL_IDENTIFIER, local_identifier]) + data
        super().__init__(data)


class REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER(AbstractKwpRequest):
    def __init__(self, local_identifier: int, data: bytearray):
        assert data, bytearray
        data = bytearray([SERVICE_TYPE.REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER, local_identifier]) + data
        super().__init__(data)


class TRANSFER_DATA(AbstractKwpRequest):
    def __init__(self, data: bytearray):
        assert data, bytearray
        data = bytearray([SERVICE_TYPE.TRANSFER_DATA]) + data
        super().__init__(data)


class REQUEST_TRANSFER_EXIT(AbstractKwpRequest):
    def __init__(self):
        data = bytearray([SERVICE_TYPE.REQUEST_TRANSFER_EXIT])
        super().__init__(data)

class REQUEST_RESET_ECU(AbstractKwpRequest):
    def __init__(self):
        data = bytearray([SERVICE_TYPE.ECU_RESET])
        super().__init__(data)


class TESTER_PRESENT(AbstractKwpRequest):
    def __init__(self):
        data = bytearray([SERVICE_TYPE.TESTER_PRESENT, 0x1])
        super().__init__(data)


class READ_DATA_BY_COMMON_IDENTIFIER(AbstractKwpRequest):
    def __init__(self):
        data = bytearray([SERVICE_TYPE.READ_DATA_BY_COMMON_IDENTIFIER, 0x0, 0x0])
        super().__init__(data)
