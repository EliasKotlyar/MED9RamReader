#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.bcm import BCM
import argparse

from src.protocols.kwp2000 import NegativeResponseError
from src.protocols.logger import Logger
if __name__ == "__main__":
    # debug = False
    

    
    logger = Logger()
    bcm = BCM(logger)
    bcm.connect()
    #bcm.writeMemory()
    
    #raise Exception("test")

    memory_address = 2000
    memory_size = 200

    CHUNK_SIZE = 100
    filename = "non-kessy.txt"    
    with open(filename, "w") as f:
        for i in range(0, memory_size, CHUNK_SIZE ):
            currentMemoryAddress = memory_address + i
            try:
                databyte = bcm.readMemory(currentMemoryAddress,CHUNK_SIZE)
                databyte = databyte.hex()
            except NegativeResponseError:
                databyte = "ERR"
                pass
            string = str(currentMemoryAddress) + ":" + databyte + "\n"
            print(string)
            f.write(string)
            f.flush()
            
    
    
