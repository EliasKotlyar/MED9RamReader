#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.med9 import MED9
import argparse
    
if __name__ == "__main__":
    debug = False
    #debug = True
    med9 = MED9(debug)
    med9.connect()

    parser = argparse.ArgumentParser(
                    prog = 'MED9RamReader',
                    description = 'Read ram of MED9',
                    epilog = '')
    parser.add_argument('address',default=0x801200)
    parser.add_argument('size',default=4)

    args = parser.parse_args()
   
    address = args.address
    size = args.size
    databyte = med9.readMemory(address,size)
    print(hex(address)+ ":" + databyte.hex())
        

        
    
    