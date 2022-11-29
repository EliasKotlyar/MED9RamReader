#!/usr/bin/env python3
import tqdm
from argparse import ArgumentParser
import time
from connections import canbus
    
if __name__ == "__main__":
    can =canbus.CANBUS()
    while(1==1):
    #    can.can_send(0x10,[0x01,0x01],100)
        frame = can.can_recv(100);
        print(frame)    
        pass
     
    
    


        

        
    
        