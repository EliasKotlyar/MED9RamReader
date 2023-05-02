#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
from src.devices.med9 import MED9
from src.protocols.logger import Logger
import argparse

if __name__ == "__main__":


    

    logger = Logger()
    
    med9 = MED9(logger)
    med9.connect()
    blockData = med9.readMeasuringBlock(115)
    print(blockData)
   
    #address = args.address
    #size = args.size
    #databyte = med9.readMemory(address,size)
    #print(hex(address)+ ":" + databyte.hex())
