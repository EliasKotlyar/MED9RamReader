#!/usr/bin/env python3
import struct
from enum import IntEnum

from src.misc.colorlogger import ColorLogger
from src.protocols.kwp2000.constants import negative_response_codes
from src.protocols.kwp2000.requests import AbstractKwpRequest
from src.protocols.kwp2000.responses import KwpResponse

from typing import NamedTuple, List
from src.protocols.logger import Logger
import logging

from src.protocols.tp20client import TP20Transport


class NegativeResponseError(Exception):
    def __init__(self, message, service_id, error_code):
        super().__init__()
        self.message = message
        self.service_id = service_id
        self.error_code = error_code

    def __str__(self):
        return self.message


class KWP_Error(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class KWP2000Client:
    def __init__(self, transport: TP20Transport):
        self.transport = transport
        self.logger = logging.getLogger("kwp")

    def send(self, kwp_request: AbstractKwpRequest) -> KwpResponse:
        send_bytes = bytes(kwp_request.to_bytes())
        self.logger.info(ColorLogger.color(f"Sending " + str(kwp_request), "pink"))
        # self.logger.warning(f"KWP TX: {send_bytes.hex()}")
        #color = "yellow"
        self.logger.info(ColorLogger.color("KWP DATA TX: " + str(send_bytes.hex()), "yellow"))

        self.transport.send(send_bytes)
        response = self.transport.recv()
        #color = "red"
        self.logger.info(ColorLogger.color("KWP DATA RX: " + str(response.hex()), "red"))
        # self.logger.warning(f"KWP RX: {response.hex()}")

        service_type = send_bytes[0]
        resp_sid = response[0]
        if service_type + 0x40 != resp_sid:
            if resp_sid in negative_response_codes:
                resp_text = negative_response_codes[resp_sid]
            else:
                resp_text = f"No Response Text for {resp_sid}"

            raise KWP_Error(resp_sid,
                            f"invalid response service id: {hex(resp_sid)} \n"
                            f"Description {resp_text} \n"
                            )
        return kwp_request.get_response(bytearray(response))
