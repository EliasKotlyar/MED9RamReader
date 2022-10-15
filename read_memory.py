#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from med9 import MED9

    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    address = 0x8043bc
    for currentAdress in range(address, address+128 ):
        databyte = med9.readMemory(currentAdress)
        print(hex(currentAdress)+ ":" + databyte.hex())
        
        
    
    