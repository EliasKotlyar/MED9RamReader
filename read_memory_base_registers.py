#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from med9 import MED9

    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    memory_address = 0x2FC100 
    memory_size = 0x50
    
    
    
    
    CHUNK_SIZE = 4
    
    
    for i in range(0, memory_size, CHUNK_SIZE ):
        databyte = med9.readMemory(memory_address + i,CHUNK_SIZE)
        print("Registers-Buffer "+ str(i/CHUNK_SIZE)+ " "  +hex(memory_address + i)+ ":" + databyte.hex())
    
    print("Finished!")
    
    