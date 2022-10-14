# Taken from https://github.com/baconwaifu/PyVCDS/blob/01e8f2fd3637b378f3200fcfe2f5a9447ee5e15a/_vw/sa2.py

class SA2:

  def calculateSA2(seed):
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
  
    