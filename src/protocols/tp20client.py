#!/usr/bin/env python3
"""
VW Transport Protoc 2.0 (TP 2.0)
Reference: https://jazdw.net/tp20
"""
import logging
import time
import struct
from typing import Optional, List, Tuple

from src.connections.canbus import CANBUS, CAN_MESSAGE
from src.misc.colorlogger import ColorLogger
from src.protocols.logger import Logger
from src.protocols.tp20.requests import *

BROADCAST_ADDR = 0x200


class MessageTimeoutError(TimeoutError):
    pass


class TP20Transport:
    def __init__(self, canbus: CANBUS, module: int, timeout: float = 0.):
        """Create TP20Transport object and open a channel"""
        self.canbus = canbus
        self.timeout = timeout
        self.msgs: List[Tuple[int, bytes]] = []
        self.sequence = 0
        self.rx_seq = 0
        self.time_between_packets = 0.0
        self.logger = logging.getLogger("tp20")
        self.open_channel(module)

    def can_recv(self, addr) -> CAN_MESSAGE:
        assert isinstance(addr, int)
        start_time = time.monotonic()
        while time.monotonic() - start_time < self.timeout:
            message = self.canbus.can_recv()
            if message is None:
                continue
            if message.id != addr:
                continue
            return message

        raise MessageTimeoutError("Timed out waiting for message")

    def increment_sequence(self):
        self.sequence = (self.sequence + 1) & 0xF

    def can_send_channel_setup(self, setup: TP20_CHANNEL_SETUP, addr: int):
        assert isinstance(setup, TP20_CHANNEL_SETUP)
        assert isinstance(addr, int)
        self.logger.info(f"TP20 Channel Setup TX: {hex(addr)} - {setup.to_bytes().hex()}")
        self.canbus.can_send(CAN_MESSAGE(addr, setup.to_bytes()))
        time.sleep(self.time_between_packets)

    def can_send_channel_params(self, parameter: TP20_CHANNEL_PARAMETER):
        assert isinstance(parameter, TP20_CHANNEL_PARAMETER)
        addr = self.tx_addr
        self.logger.info(f"TP20 Parameter Setup TX: {hex(addr)} - {parameter.to_bytes().hex()}")
        self.canbus.can_send(CAN_MESSAGE(addr, parameter.to_bytes()))
        time.sleep(self.time_between_packets)

    def can_send_data(self, data: TP20_DATA):
        self.canbus.can_send(CAN_MESSAGE(self.tx_addr, data.to_bytes()))
        color = "blue"
        self.logger.info(ColorLogger.color("TP20 DATA TX: " + str(data), color))

        # self.logger.info()
        # self.logger.info(f"TP20 DATA TX: {data.to_bytes().hex()}")
        time.sleep(self.time_between_packets)

    def open_channel(self, module: int):
        """Before communicating to an ECU we have to open a channel.
        This is done on the broadcast address of 0x200. We expect a
        reply on 0x200 + module logial address. We ask the destination module
        to broadcast on 0x300. It will reply with an address for us to transmit on."""
        module = TP20_CHANNEL_SETUP_LOGICAL_ADDR.MOTOR
        cmd = TP20_CHANNEL_SETUP(
            logical_addr=module,
            setup_request=TP20_CHANNEL_OPCode.SETUP_REQUEST,
            rx_id=0x100,
            tx_id=0x300,
            protocol_type=0x01
        )

        self.can_send_channel_setup(cmd, BROADCAST_ADDR)
        can_msg = self.can_recv(BROADCAST_ADDR + module)
        response = TP20_CHANNEL_SETUP.from_bytes(can_msg.data)
        assert response.setup_request == TP20_CHANNEL_OPCode.POSITIVE_RESPONSE
        assert response.rx_id == 0x300  # We asked for this

        self.rx_addr = response.rx_id
        self.tx_addr = response.tx_id

        cmd = TP20_CHANNEL_PARAMETER(
            opcode=TP20_CHANNEL_PARAMETER_OPCode.PARAMETERS_REQUEST,
            block_size=0x0f,
            timing_param1=0x8a,
            timing_param2=0xff,
            timing_param3=0x0a,
            timing_param4=0xff
        )
        self.can_send_channel_params(cmd)
        can_msg = self.can_recv(self.rx_addr)
        response = TP20_CHANNEL_PARAMETER.from_bytes(can_msg.data)
        assert response.opcode == TP20_CHANNEL_PARAMETER_OPCode.PARAMETERS_RESPONSE

        self.time_between_packets = 0.01
        self.sequence = 0
        self.rx_seq = 0

    def wait_for_ack(self):
        """Even though both sides have their own sequence counter
        we expect an ack with our own sequence + 1"""
        # self.increment_tx_ctr()
        response = self.can_data_recv()
        if response.opcode != TP20_DATA_OPCODES.ACK_READY_FOR_NEXT_PACKET:
            raise RuntimeError(f"Wrong Opcode received: {response.opcode}")

        # seq = (self.tx_seq) & 0xF
        # if response.sequence != seq:
        #    raise RuntimeError(f"Wrong Sequence received. Received: {response.sequence}.  Expected: {seq}")

    def send_ack(self, lastsequence: int):
        lastsequence = (lastsequence + 1) & 0xF
        cmd = TP20_DATA(TP20_DATA_OPCODES.ACK_READY_FOR_NEXT_PACKET, lastsequence, bytearray([]))
        self.can_send_data(cmd)

    def send(self, dat: bytes):
        """Sends longer string of data by dividing into smaller chunks
        and waiting for acknowledge after the last chunk"""
        if len(dat) > 0xFF:
            raise ValueError("Packet longer than 255 bytes not supported")

        # Prepend length
        payload = struct.pack(">H", len(dat)) + dat

        while payload:
            last = len(payload) <= 7
            payload_to_send = payload[:7]
            if last:
                opcode = TP20_DATA_OPCODES.WAITING_FOR_ACK_LAST_PACKET
            else:
                opcode = TP20_DATA_OPCODES.NOT_WAITING_FOR_ACK_MORE_PACKETS

            cmd = TP20_DATA(opcode, self.sequence, bytearray(payload_to_send))
            self.can_send_data(cmd)
            self.increment_sequence()

            if last:
                self.wait_for_ack()

            payload = payload[7:]

    def can_data_recv(self) -> TP20_DATA:

        t = self.rx_seq
        raw_can_data = self.can_recv(self.rx_addr)
        payload = raw_can_data.data
        if len(payload) == 1:
            for member in TP20_CHANNEL_PARAMETER_OPCode:
                if member.value == payload[0]:
                    raise Exception(f'Received Opcode {member.name} ({hex(member.value)})')

        response = TP20_DATA.from_bytes(payload)

        color = "green"

        self.logger.info(ColorLogger.color("TP20 DATA RX: " + str(response), color))
        return response

    def recv(self) -> bytes:
        """Receives multiple chunks of a response and combines
        them into a single string"""
        payload = b""
        while True:
            response = self.can_data_recv()
            payload += response.payload
            # self.logger.info(f"Payload: {response.payload.hex()}")
            if response.opcode == TP20_DATA_OPCODES.WAITING_FOR_ACK_LAST_PACKET:
                # Last packet, send ack and return data
                self.send_ack(response.sequence)
                break
        length = struct.unpack(">H", payload[:2])[0]
        data = payload[2: length + 2]
        # assert len(data) == length
        return data

    def keepChannelAlive(self):
        cmd = TP20_CHANNEL_PARAMETER(
            opcode=TP20_CHANNEL_PARAMETER_OPCode.CHANNEL_TEST,
        )
        self.can_send_raw(cmd.to_bytes())
        self.can_recv()
