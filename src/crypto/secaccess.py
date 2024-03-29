from src.crypto.sa_seed_key import Sa2SeedKey
class SecurityAccessInterface:
    PROGRAMMING = 0x01
    NORMAL = 0x02
    def getAccessType() -> int:
        pass
    def calculate(self, seed: int) -> int:
        """Extract text from the currently loaded file."""
        pass

class SA2(SecurityAccessInterface):
    def getAccessType(self) -> int:
        return self.PROGRAMMING
    def calculate(self, seed: int) -> int:
        seedData = 0x5FBD5DBD
        #note: original java implementation used an "unsigned shift" for the rshift, but python numbers don't "have" a visible sign bit
        #and as such can be treated as pure u32.
        # (seed << 1) | (seed >> 31) is bitwise left rotate, by ORing the MSBit to the left-shift.
        for i in range(5): #5 shifts
            if ((seed & 0x80000000) == 0x80000000): # if the "to overflow" bit is set, xor with 'key'
                seed = (seedData) ^ ((seed << 1) | (seed >> 31)) & 0xffffffff # rotate left, xor, and clamp.
            else:
                seed = ((seed << 1) | (seed >> 31)) #rotate left only  
        return seed
    
class MED91_READ_ACCESS(SecurityAccessInterface):
    def getAccessType(self) -> int:
            return self.NORMAL
    def calculate(self, seed: int) -> int:
        return seed + 0x00011170

class MED91_WRITE_ACCESS(SA2):
    def getAccessType(self) -> int:
        return self.PROGRAMMING
    

class BCM_READ_ACCESS(SecurityAccessInterface):
    def getAccessType(self) -> int:
            return self.NORMAL
    def calculate(self, seed: int) -> int:
        return seed + 42063    
    
class BCM_WRITE_ACCESS(SecurityAccessInterface):
    def getAccessType(self) -> int:
             return self.PROGRAMMING
    def calculate(self, seed: int) -> int:
        hex_string = "81 4A 0A 84 00 00 00 01 87 04 C1 1D B7 81 4A 07 87 04 C1 1D B7 6B 05 93 00 00 00 01 81 4A 0A 84 00 00 00 01 87 04 C1 1D B7 81 4A 07 87 04 C1 1D B7 6B 05 93 00 00 00 01 81 4A 0A 84 00 00 00 01 87 04 C1 1D B7 81 4A 0A 84 00 00 00 01 87 04 C1 1D B7 81 4A 07 87 04 C1 1D B7 6B 05 93 00 00 00 01 81 4A 0A 84 00 00 00 01 87 04 C1 1D B7 4C"
        byteStr = bytearray.fromhex(hex_string)
        vs = Sa2SeedKey(byteStr, seed)
        return vs.execute()

        
    
