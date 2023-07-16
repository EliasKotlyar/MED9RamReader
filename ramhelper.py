#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.med9 import MED9
from src.protocols.logger import Logger
import argparse

if __name__ == "__main__":
    logger = Logger()

    med9 = MED9(logger)

    med9.connect()
    # blockData = med9.readMeasuringBlock(115)
    # print(blockData)

    address = 0x803980
    size = 100
    med9.dynamicallyDefineIdentifier(0xF2, 0x111111, 0x12)
    med9.dynamicallyDefineIdentifier(0xF3, 0x222222, 0x23)

    databyte = med9.readMemory(address, size)
    print(hex(address) + ":" + databyte.hex())
