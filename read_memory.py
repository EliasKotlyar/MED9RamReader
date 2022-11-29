#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from med9 import MED9

    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    address = 0x007fc99a
    databyte = med9.readMemory(address,4)
    print(hex(address)+ ":" + databyte.hex())
        

        
    
    