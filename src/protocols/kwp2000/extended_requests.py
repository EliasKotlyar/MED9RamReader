from requests import READ_ECU_IDENTIFICATION, AbstractKwpRequest


class IDENT_9B(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        payload = bytearray([
            0x0
        ])
        ret = READ_ECU_IDENTIFICATION(0x9B, payload)
        return ret.to_bytes()


class IDENT_9C(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        payload = bytearray([
            0x0
        ])
        ret = READ_ECU_IDENTIFICATION(0x9B, payload)
        return ret.to_bytes()


class START_DIAGNOSTIC_SESSION_FLASH(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        payload = bytearray([
            0x0
        ])
        ret = START_DIAGNOSTIC_SESSION_FLASH()
        return ret.to_bytes()


class REQUEST_SEED(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        payload = bytearray([
            0x0
        ])
        ret = START_DIAGNOSTIC_SESSION_FLASH()
        return ret.to_bytes()

class SEND_KEY(AbstractKwpRequest):
    def __init__(self):
        super().__init__()

    def to_bytes(self):
        payload = bytearray([
            0x0
        ])
        ret = START_DIAGNOSTIC_SESSION_FLASH()
        return ret.to_bytes()