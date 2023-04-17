#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.med9 import MED9
from src.crypto.xor import Xor
from src.protocols.logger import Logger
if __name__ == "__main__":

    logger = Logger()
    med9 = MED9(logger)
    med9.connect()
    address = 0x8043bc
    #oldValue = med9.readMemory(address,4)
    #print("Memory:")
    #print(oldValue.hex())
    #med9.readMemoryByUpload(address,4)
    med9.writeMemoryByUpload(address,bytes([0x0,0x0,0x0,0x0]))
    #xor = Xor()
    #print(xor.encrypt(bytes([0x41,0x4D,0x54,0x20,0x20,0x20,0x20,0x20,0x20,0x20,0x20]),"RobertCode").hex())
    