#!/usr/bin/env python3
import struct
from enum import IntEnum

from src.protocols.kwp2000.requests import AbstractKwpRequest
from src.protocols.kwp2000.responses import KwpResponse
from src.protocols.tp20 import TP20Transport
from typing import NamedTuple, List
from src.protocols.logger import Logger
import logging


class NegativeResponseError(Exception):
    def __init__(self, message, service_id, error_code):
        super().__init__()
        self.message = message
        self.service_id = service_id
        self.error_code = error_code

    def __str__(self):
        return self.message


class InvalidServiceIdError(Exception):
    pass


class InvalidSubFunctionError(Exception):
    pass


class KWP2000Client:
    def __init__(self, transport: TP20Transport):
        self.transport = transport
        self.logger = logging.getLogger("kwp")

    def send(self, kwp_request: AbstractKwpRequest) -> KwpResponse:
        send_bytes = bytes(kwp_request.to_bytes())
        self.logger.warning(f"Sending " + str(kwp_request))
        self.logger.warning(f"KWP TX: {send_bytes.hex()}")
        self.transport.send(send_bytes)
        response = self.transport.recv()
        self.logger.warning(f"KWP RX: {response.hex()}")

        service_type = send_bytes[0]
        resp_sid = response[0]
        if service_type + 0x40 != resp_sid:
            resp_sid = resp_sid - 0x40 - service_type
            resp_sid_hex = hex(resp_sid)
            raise InvalidServiceIdError("invalid response service id: {}".format(resp_sid_hex))
        return kwp_request.get_response(bytearray(response))
