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
    memory_size = 100
    filename = "dump.bin"
    print("Dumping Memmory...")
    
    progress = tqdm.tqdm(total=memory_size)
    with open(filename, "wb") as f:
        for i in range(0, memory_size ):
            databyte = med9.readMemory(i+memory_address)
            f.write(databyte)
            f.flush()
            progress.update(1)
            #print(hex(currentAdress)+ ":" + databyte.hex())
        progress.close()
    print("Finished!")
    
    