from __future__ import annotations
from enum import IntEnum

from bitstring import BitArray


class TP20_CHANNEL_PARAMETER_OPCode(IntEnum):
    PARAMETERS_REQUEST = 0xA0
    PARAMETERS_RESPONSE = 0xA1
    CHANNEL_TEST = 0xA3
    BREAK = 0xA4
    DISCONNECT = 0xA8


class TP20_CHANNEL_PARAMETER_ONEBYTE:
    def __init__(self, opcode: TP20_CHANNEL_PARAMETER_OPCode):
        assert isinstance(opcode, TP20_CHANNEL_PARAMETER_OPCode), "opcode must be an integer"
        self.opcode = opcode

    def to_bytes(self) -> bytearray:
        return bytearray([
            self.opcode,
        ])


class TP20_CHANNEL_PARAMETER:
    def __init__(self, opcode: TP20_CHANNEL_PARAMETER_OPCode,
                 block_size: int,
                 timing_param1: int,
                 timing_param3: int, ):
        assert isinstance(opcode, TP20_CHANNEL_PARAMETER_OPCode), "opcode must be an integer"
        assert isinstance(block_size, int), "block_size must be an integer"
        self.opcode = opcode
        self.block_size = block_size
        self.timing_param1 = timing_param1
        self.timing_param2 = 0xff
        self.timing_param3 = timing_param3
        self.timing_param4 = 0xff

    def to_bytes(self) -> bytearray:
        return bytearray([
            self.opcode,
            self.block_size,
            self.timing_param1,
            self.timing_param2,
            self.timing_param3,
            self.timing_param4,
        ])

    @classmethod
    def from_bytes(cls, data: bytes) -> TP20_CHANNEL_PARAMETER:
        assert len(data) == 6 or len(data) == 1, "Invalid data length for TP20ChannelParameters"
        if len(data) == 6:
            opcode, block_size, timing_param1, timing_param2, timing_param3, timing_param4 = data
        else:
            opcode = data[0]
            block_size, timing_param1, timing_param2, timing_param3, timing_param4 = 0, 0, 0, 0, 0

        return cls(
            opcode=TP20_CHANNEL_PARAMETER_OPCode(opcode),
            block_size=block_size,
            timing_param1=timing_param1,
            timing_param3=timing_param3,
        )
