from __future__ import annotations

from enum import IntEnum

from bitstring import BitArray


class TP20_CHANNEL_SETUP_LOGICAL_ADDR(IntEnum):
    RESPONSE = 0x0
    MOTOR = 0x01


class TP20_CHANNEL_OPCode(IntEnum):
    SETUP_REQUEST = 0xC0
    POSITIVE_RESPONSE = 0xD0
    NEGATIVE_RESPONSE1 = 0xD6
    NEGATIVE_RESPONSE2 = 0xD7
    NEGATIVE_RESPONS3 = 0xD8


class TP20_CHANNEL_PROTOCOL_TYPES(IntEnum):
    KWP = 0x01


class TP20_CHANNEL_SETUP():
    def __init__(self, logical_addr: TP20_CHANNEL_SETUP_LOGICAL_ADDR, setup_request: TP20_CHANNEL_OPCode, rx_id: int,
                 tx_id: int,
                 protocol_type: TP20_CHANNEL_PROTOCOL_TYPES):
        assert isinstance(logical_addr, TP20_CHANNEL_SETUP_LOGICAL_ADDR), "logical_addr must be an integer"
        assert isinstance(setup_request, TP20_CHANNEL_OPCode), "setup_request must be an integer"
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
            logical_addr=TP20_CHANNEL_SETUP_LOGICAL_ADDR(logical_addr),
            setup_request=TP20_CHANNEL_OPCode(setup_request),
            rx_id=rx,
            tx_id=tx,
            protocol_type=TP20_CHANNEL_PROTOCOL_TYPES(protocol_type)
        )
