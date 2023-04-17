#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.bcm import BCM
import argparse

from src.protocols.kwp2000 import NegativeResponseError

if __name__ == "__main__":
    # debug = False
    

    debug = False
    bcm = BCM(debug)
    bcm.connect()

    memory_address = 0
    memory_size = 20000

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
            
    
    
