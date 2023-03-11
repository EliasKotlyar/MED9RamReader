#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.med9 import MED9

    
if __name__ == "__main__":
    debug = False
    debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    address = 0x8043bc
    oldValue = med9.readMemory(address)
    print("Old Value:")
    print(hex(address)+ ":" + oldValue.hex())
    
    print("New Value:")
    value = 0xFF
    # Somehow this is broken and always returns WRITE_DATA_BY_LOCAL_IDENTIFIER - subFunctionNotSupported-invalidFormat
    med9.writeMemory(address,value)
    newValue = med9.readMemory(address)
    print(hex(address)+ ":" + newValue.hex())
    
    
        
        
        
    
    