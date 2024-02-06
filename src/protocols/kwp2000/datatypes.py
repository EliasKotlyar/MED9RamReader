from bitstring import BitArray


class FlashToolCode(bytearray):
    def __init__(self, value: str):
        assert len(value) == 6
        bytes = value.encode('ascii')
        assert len(bytes) == 6
        super().__init__(bytes)


class Int32Bit(bytearray):
    def __init__(self, value: int):
        assert isinstance(value, int)
        bytes = BitArray(uintbe=value, length=32).tobytes()
        super().__init__(bytes)


class Int24Bit(bytearray):
    def __init__(self, value: int):
        assert isinstance(value, int)
        bytes = BitArray(uintbe=value, length=24).tobytes()
        super().__init__(bytes)


class Int16Bit(bytearray):
    def __init__(self, value: int):
        assert isinstance(value, int)
        bytes = BitArray(uintbe=value, length=16).tobytes()
        super().__init__(bytes)


class Int8Bit(bytearray):
    def __init__(self, value1: int, value2: int):
        assert isinstance(value1, int)
        assert isinstance(value2, int)
        bytes = BitArray(uint=0, length=8)
        bytes[0:4] = value1
        bytes[4:8] = value2
        super().__init__(bytes.tobytes())
