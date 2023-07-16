#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.med9 import MED9
import argparse
from src.protocols.logger import Logger

if __name__ == "__main__":
    # debug = False

    parser = argparse.ArgumentParser(
        prog='MED9RamReader',
        description='Read ram of MED9',
        epilog='')
    parser.add_argument('--address', default=0x801200, required=False)
    parser.add_argument('--size', default=4, required=False)

    args = parser.parse_args()


    debug = True
    logger = Logger()
    med9 = MED9(logger)
    try:
        med9.connect()
        address = args.address
        size = args.size
        databyte = med9.readMemoryByAddress(address, size)
        print(hex(address) + ":" + databyte.hex())
    finally:
        med9.disconnect()

