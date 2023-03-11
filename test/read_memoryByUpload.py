#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.med9 import MED9

    
if __name__ == "__main__":
    debug = False
    debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    address = 0x480000
    databyte = med9.readMemoryRequestUpload(address,0x200000)
    print(hex(address)+ ":" + databyte.hex())
        
        
    
    