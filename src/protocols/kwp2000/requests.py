from constants import SERVICE_TYPE


class AbstractKwpRequest:
    def __init__(self):
        pass

    def to_bytes(self) -> bytearray:
        raise NotImplementedError("Subclasses must implement the to_bytes method")


class READ_ECU_IDENTIFICATION(AbstractKwpRequest):
    def __init__(self, RoutineLocalIdentifier: int, data: bytearray):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.READ_ECU_IDENTIFICATION])


class START_DIAGNOSTIC_SESSION(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.START_DIAGNOSTIC_SESSION])


class SECURITY_ACCESS(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.SECURITY_ACCESS])


class REQUEST_DOWNLOAD(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.REQUEST_DOWNLOAD])


class START_ROUTINE_BY_LOCAL_IDENTIFIER(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.START_ROUTINE_BY_LOCAL_IDENTIFIER])


class REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER])


class TRANSFER_DATA(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.TRANSFER_DATA])


class REQUEST_TRANSFER_EXIT(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        return bytearray([SERVICE_TYPE.REQUEST_TRANSFER_EXIT])
