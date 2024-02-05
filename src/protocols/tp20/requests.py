from __future__ import annotations
from enum import IntEnum

from bitstring import BitArray


class TP20_CHANNEL_SETUP_LOGICAL_ADDR(IntEnum):
    MOTOR = 0x01


class TP20_CHANNEL_OPCode(IntEnum):
    SETUP_REQUEST = 0xC0
    POSITIVE_RESPONSE = 0xD0
    NEGATIVE_RESPONSE1 = 0xD6
    NEGATIVE_RESPONSE2 = 0xD7
    NEGATIVE_RESPONS3 = 0xD8


class TP20_CHANNEL_SETUP():
    def __init__(self, logical_addr: TP20_CHANNEL_SETUP_LOGICAL_ADDR, setup_request: TP20_CHANNEL_OPCode, rx_id: int,
                 tx_id: int,
                 protocol_type: int):
        assert isinstance(logical_addr, int), "logical_addr must be an integer"
        assert isinstance(setup_request, int), "setup_request must be an integer"
        self.logical_addr = logical_addr
        self.setup_request = setup_request
        self.rx_id = rx_id
        self.tx_id = tx_id
        self.protocol_type = protocol_type

    def to_bytes(self) -> bytearray:
        rx = BitArray(uint=self.rx_id, length=16)
        tx = BitArray(uint=self.tx_id, length=16)

        return bytearray([
            self.logical_addr,
            self.setup_request,  # Setup Request
            rx[8:].int,  # RX ID
            rx[:8].int,  # RX_pref
            tx[8:].int,  # TX ID
            tx[:8].int,  # TX_pref
            self.protocol_type,  # Protocol Type
        ])

    @classmethod
    def from_bytes(cls, data: bytes) -> TP20_CHANNEL_SETUP:
        assert len(data) == 7, "Invalid data length for TP20ChannelSetup"
        logical_addr, setup_request, rx_id, rx_pref, tx_id, tx_pref, protocol_type = data
        tx = (tx_pref << 8) | tx_id
        rx = (rx_pref << 8) | rx_id

        return cls(
            logical_addr=logical_addr,
            setup_request=setup_request,
            rx_id=rx,
            tx_id=tx,
            protocol_type=protocol_type
        )


class TP20_CHANNEL_PARAMETER_OPCode(IntEnum):
    PARAMETERS_REQUEST = 0xA0
    PARAMETERS_RESPONSE = 0xA1
    CHANNEL_TEST = 0xA3
    BREAK = 0xA4
    DISCONNECT = 0xA8


class TP20_CHANNEL_PARAMETER:
    def __init__(self, opcode: int,
                 block_size: int,
                 timing_param1: int,
                 timing_param2: int,
                 timing_param3: int,
                 timing_param4: int):
        assert isinstance(opcode, int), "opcode must be an integer"
        assert isinstance(block_size, int), "block_size must be an integer"
        self.opcode = opcode
        self.block_size = block_size
        self.timing_param1 = timing_param1
        self.timing_param2 = timing_param2
        self.timing_param3 = timing_param3
        self.timing_param4 = timing_param4

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
            opcode=opcode,
            block_size=block_size,
            timing_param1=timing_param1,
            timing_param2=timing_param2,
            timing_param3=timing_param3,
            timing_param4=timing_param4
        )


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
