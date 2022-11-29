#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from med9 import MED9

    
if __name__ == "__main__":
    debug = False
    # debug = True
    med9 = MED9("can0",debug)
    med9.connect()
    memory_address = 0x800000
    memory_size = 0x4B60
    

    filename = "dump.bin"
    print("Dumping Memmory...")
    CHUNK_SIZE = 50
    progress = tqdm.tqdm(total=memory_size)
    with open(filename, "wb") as f:
        for i in range(0, memory_size, CHUNK_SIZE ):
            databyte = med9.readMemory(memory_address + i,CHUNK_SIZE)
            f.write(databyte)
            f.flush()
            progress.update(CHUNK_SIZE)
            #print(hex(currentAdress)+ ":" + databyte.hex())
        progress.close()
    print("Finished!")
    
    