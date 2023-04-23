# MED9RamReader
Utility to read Ram of a MED9.1 ECU

## Requirements:
Linux: 
SocketCan capable Adapter

Windows:
OpenPort 2.0 Adapter
Python (32 Bit)

## Usage

2. Run pip install -r requirements.txt
2. Run read_memory.py for reading a part of memory.

Attention: The code is highly experimental and may break your ECU if used incorrectly.

## Adding new device:

1. Find a suitable SGO-Binary
2. Use VagHelperX to idenfitify SA2 Sequence
3. Insert SA2 Sequence into secaccess.py file
4. Use functions

### Credits
Most of the code is based on the awesome work of https://github.com/pd0wm/pq-flasher. Many thanks!
