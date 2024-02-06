from __future__ import annotations



class BinaryDump:
    def __init__(self, content):
        '''
        Initializes a BinaryDump object with the provided content.

        Parameters:
        - content: Initial content for the BinaryDump.
        '''
        self._array = bytearray(content)
        self._size = len(content)

    def get_part(self, address: int, size: int):
        '''
        Retrieves a part of the BinaryDump starting from the specified address.

        Parameters:
        - address (HexAddress): Starting address for the part.
        - size (int): Size of the part to retrieve.

        Returns:
        - BinaryDump: A new BinaryDump containing the specified part.
        '''
        assert isinstance(address, int)
        assert isinstance(size, int)
        adr = address
        return BinaryDump(self._array[adr:adr + size])

    def hex(self):
        '''
        Returns the hexadecimal representation of the BinaryDump content.

        Returns:
        - str: Hexadecimal representation.
        '''
        return self._array.hex().upper()

    def __str__(self):
        '''
        Returns the hexadecimal representation when the object is converted to a string.

        Returns:
        - str: Hexadecimal representation.
        '''
        return self.hex()



    def get_bytes(self):
        return self._array
