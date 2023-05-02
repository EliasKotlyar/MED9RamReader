
class MeasuringBlock:
    number : int
    identNumber : int
    a : int
    b : int
    def __init__(self,number, data:bytes):
        self.number = number
        self.identNumber = data[0]
        self.a = data[1]
        self.b = data[2]
        pass
    def __str__(self) -> str:
        #retStr = "(i: 0x{:X}, a : 0x{:X}, b : 0x{:X})".format(self.identNumber,self.a,self.b)

        form = FormulaConverter()
        retStr = form.conversion(self.identNumber,self.a,self.b)
        #retStr = (self.b-128)/(0.01*self.a)
        #retStr = (256* self.a + self.b)*0.3254
        return str("Block "+str(self.number) + ": "+ retStr + "\r\n")

class MeasuringBlockGroup:
    number : int
    blocks = [] 
    def __init__(self,data:bytes):
        print(data.hex())
        for blockNumber in range(0,4):
            blockData = data[blockNumber * 3:blockNumber * 3 +3]
            block = MeasuringBlock((blockNumber + 1),blockData)
            self.blocks.append(block)
    def __str__(self):
        retStr = ""
        for block in self.blocks:
            retStr = retStr + block.__str__()
        return retStr

        

class FormulaConverter:
    def conversion(self, k, a, b):
        if k == 1:
            v = 0.2 * a * b
            units = "rpm"
        elif k == 2:
            v = a * 0.002 * b
            units = "%"
        elif k == 3:
            v = 0.002 * a * b
            units = "Deg"
        elif k == 4:
            v = abs(b - 127) * 0.01 * a
            units = "ATDC"
        elif k == 5:
            v = a * (b - 100) * 0.1
            units = "c"
        elif k == 6:
            v = 0.001 * a * b
            units = "v"
        elif k == 7:
            v = 0.01 * a * b
            units = "km/h"
        elif k == 8:
            v = 0.1 * a * b
            units = " "
        elif k == 9:
            v = (b - 127) * 0.02 * a
            units = "Deg"
        elif k == 10:
            if b == 0:
                t = "COLD"
            else:
                t = "WARM"
        elif k == 11:
            v = 0.0001 * a * (b - 128) + 1
            units = " "
        elif k == 12:
            v = 0.001 * a * b
            units = "Ohm"
        elif k == 13:
            v = (b - 127) * 0.001 * a
            units = "mm"
        elif k == 14:
            v = 0.005 * a * b
            units = "bar"
        elif k == 15:
            v = 0.01 * a * b
            units = "ms"
        elif k == 18:
            v = 0.04 * a * b
            units = "mbar"
        elif k == 19:
            v = a * b * 0.01
            units = "l"
        elif k == 20:
            v = a * (b - 128) / 128
            units = "%"
        elif k == 21:
            v = 0.001 * a * b
            units = "V"
        elif k == 22:
            v = 0.001 * a * b
            units = "ms"
        elif k == 23:
            v = b / 256 * a
            units = "%"
        elif k == 24:
            v = 0.001 * a * b
            units = "A"
        elif k == 25:
            v = (b * 1.421) + (a / 182)
            units = "g/s"
        elif k == 26:
            v = float(b - a)
            units = "C"
        elif k == 27:
            v = abs(b - 128) * 0.01 * a
            units = "Deg"
        elif k == 28:
            v = float(b - a)
            units = " "
        elif k == 30:
            v = b / 12 * a
            units = "Deg k/w"
        elif k == 31:
            v = b / 2560 * a
            units = "°C"
        # start at case 33
        if k == 33:
            v = 100 * b / a
            units = "%%"
        elif k == 34:
            v = (b - 128) * 0.01 * a
            units = "kW"
        elif k == 35:
            v = 0.01 * a * b
            units = "l/h"
        elif k == 36:
            v = int(a) * 2560 + int(b) * 10
            units = "km"
        elif k == 37:
            # Broken!!
            v = b
        elif k == 38:
            v = (b - 128) * 0.001 * a
            units = "Deg k/w"
        elif k == 39:
            v = b / 256 * a
            units = "mg/h"
        elif k == 40:
            v = b * 0.1 + (25.5 * a) - 400
            units = "A"
        elif k == 41:
            v = b + a * 255
            units = "Ah"
        elif k == 42:
            v = b * 0.1 + (25.5 * a) - 400
            units = "Kw"
        elif k == 43:
            v = b * 0.1 + (25.5 * a)
            units = "V"
        elif k == 44:
            buf = "{:02d}:{:02d}".format(a, b)
            t = buf
        elif k == 45:
            v = 0.1 * a * b / 100
            units = " "
        elif k == 46:
            v = (a * b - 3200) * 0.0027
            units = "Deg k/w"
        elif k == 47:
            v = (b - 128) * a
            units = "ms"
        elif k == 48:
            v = b + a * 255
            units = " "
        elif k == 49:
            v = (b / 4) * a * 0.1
            units = "mg/h"
        elif k == 50:
            v = (b - 128) / (0.01 * a)
            units = "mbar"
        elif k == 51:
            v = ((b - 128) / 255) * a
            units = "mg/h"
        elif k == 52:
            v = b * 0.02 * a - a
            units = "Nm"
        elif k == 53:
            v = (b - 128) * 1.4222 + 0.006 * a
            units = "g/s"
        elif k == 54:
            v = a * 256 + b
            units = "count"
        elif k == 55:
            v = a * b / 200
            units = "s"
        elif k == 56:
            v = a * 256 + b
            units = "WSC"
        elif k == 57:
            v = a * 256 + b + 65536
            units = "WSC"
        elif k == 59:
            v = (a * 256 + b) / 32768
            units = "g/s"
        elif k == 60:
            v = (a * 256 + b) * 0.01
            units = "sec"
        elif k == 62:
            v = 0.256 * a * b
            units = "S"
        elif k == 64:
            v = float(a + b)
            units = "Ohm"
        elif k == 65:
            v = 0.01 * a * (b - 127)
            units = "mm"
        elif k == 66:
            v = (a * b) / 511.12
            units = "V"
        elif k == 67:
            v = (640 * a) + b * 2.5
            units = "Deg"
        elif k == 68:
            v = (256 * a + b) / 7.365
            units = "deg/s"
        elif k == 69:
            v = (256 * a + b) * 0.3254
            units = "Bar"
        elif k == 70:
            v = (256 * a + b) * 0.192
            units = "m/s^2"
        elif k == 96:
            v = 0.1 * a * b
            units = " "
        else:
            v = "{}, {}      ".format(hex(a), hex(b))
            units = "(no unit)"

        return str(v) + str(units)