#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from med9 import MED9

    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9(debug)
    med9.connect()
    
    address = 0x801200
    #value = 0x1050305
    
    #address = 0x5c6338
    value = 0x57cc0739
    
    #med9.writeRamCustomMethod(address,value)
    
    databyte = med9.readMemory(address,4)
    print(hex(address)+ ":" + databyte.hex())
        

        
    
    