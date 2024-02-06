from __future__ import annotations
from enum import IntEnum

from bitstring import BitArray


class TP20_DATA_OPCODES(IntEnum):
    WAITING_FOR_ACK_MORE_PACKETS = 0x0
    WAITING_FOR_ACK_LAST_PACKET = 0x1
    NOT_WAITING_FOR_ACK_MORE_PACKETS = 0x2
    NOT_WAITING_FOR_ACK_LAST_PACKET = 0x3
    ACK_READY_FOR_NEXT_PACKET = 0xB
    ACK_NOT_READY_FOR_NEXT_PACKET = 0x9


class TP20_DATA:
    def __init__(self, opcode: TP20_DATA_OPCODES, sequence: int, payload: bytearray):
        # print(sequence)
        assert isinstance(opcode, TP20_DATA_OPCODES), "opcode must be of type TP20_DATA_OPCODES"
        assert isinstance(sequence, int), "sequence must be an integer"
        assert isinstance(payload, bytearray), "payload must be a bytes object"
        self.opcode = opcode
        self.sequence = sequence
        self.payload = bytearray(payload)

    def to_bytes(self) -> bytearray:
        byte0 = BitArray(uint=0, length=8)
        byte0[:4] = self.opcode
        byte0[4:] = self.sequence
        return bytearray(byte0.tobytes() + self.payload)

    @classmethod
    def from_bytes(cls, data: bytes) -> TP20_DATA:
        assert len(data) >= 1, "Invalid data length for TP20_DATA"
        byte0 = BitArray(uint=data[0], length=8)
        sequence = byte0[4:8].uint
        opcode = byte0[0:4].uint
        payload = bytearray(data[1:])
        return cls(
            opcode=TP20_DATA_OPCODES(opcode),
            sequence=sequence,
            payload=payload
        )

    def __str__(self):
        return (
            f"  Sequence: {self.sequence} "
            f"  Opcode: {self.opcode.name} ({hex(self.opcode.value)}) "
            f"  Payload: {self.payload.hex()} "
        )
