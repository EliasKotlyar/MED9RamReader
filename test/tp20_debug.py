#!/usr/bin/env python3
from src.connections import canbus
from src.protocols.tp20debug import TP20Debug

if __name__ == "__main__":
    bus = canbus.CANBUS()
    tp20 = TP20Debug(bus)
    while 1:
        packet = tp20.recv()
        print(packet)


