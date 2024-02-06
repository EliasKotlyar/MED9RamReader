#!/usr/bin/env python3
import struct
from enum import IntEnum

from src.misc.colorlogger import ColorLogger
from src.protocols.kwp2000.constants import NegativeResponseCode
from src.protocols.kwp2000.requests import AbstractKwpRequest
from src.protocols.kwp2000.responses import KwpResponse, KwpNegativeResponse

from typing import NamedTuple, List
import logging

from src.protocols.tp20client import TP20Transport


class KWP_Exception(Exception):
    def __init__(self, response: KwpNegativeResponse):
        assert isinstance(response, KwpNegativeResponse)
        super().__init__(str(response))
        self.code = response.code


class KWP2000Client:
    def __init__(self, transport: TP20Transport):
        self.transport = transport
        self.logger = logging.getLogger("kwp")

    def send(self, kwp_request: AbstractKwpRequest, throwException: bool = True):
        send_bytes = bytes(kwp_request.to_bytes())
        self.logger.info(ColorLogger.color(f"Sending " + str(kwp_request), "pink"))
        # self.logger.warning(f"KWP TX: {send_bytes.hex()}")

        self.logger.info(ColorLogger.color("KWP DATA TX: " + str(send_bytes.hex()), "yellow"))
        self.transport.send(send_bytes)
        while True:
            response = self.transport.recv()
            self.logger.info(ColorLogger.color("KWP DATA RX: " + str(response.hex()), "red"))
            service_type = send_bytes[0]
            resp_sid = response[0]
            if service_type + 0x40 == resp_sid:
                response = kwp_request.get_positive_response(bytearray(response))
                break
            else:
                response = kwp_request.get_negative_response(bytearray(response))
                if response.code == NegativeResponseCode.requestCorrectlyReceived_ResponsePending:
                    continue
                else:
                    if throwException == True:
                        raise KWP_Exception(response)

        return response
