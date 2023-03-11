#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.med9 import MED9
import time
    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    memory_address = 0x804152
    memory_size = 0x70
    
    
    filename = "dump.bin"
    print("Dumping Memmory...")
    CHUNK_SIZE = 12
    
    
    for i in range(0, memory_size, CHUNK_SIZE ):
        #med9.sendRawCanBusMessage(0x539,[0,3,3,4,5,6,7,8],1)
        #time.sleep(1)
        databyte = med9.readMemory(memory_address + i,CHUNK_SIZE)
        print("CAN-Buffer "+ str(i/CHUNK_SIZE + 1)+ " "  +hex(memory_address + i)+ ":" + databyte.hex())
    
    print("Finished!")
    
    