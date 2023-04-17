# Some common passwords are BiWbBuD101, GEHEIM, CodeRobert, MILKYWAY
class Xor:
    def encrypt(self, data: bytes, key: str) -> bytes:
        byteKey = str.encode(key)
        output_data = bytearray()
        counter = 0
        for data_byte in data:
            currentXor = byteKey[counter]
            output_data.append(data_byte ^ currentXor)
            counter += 1
            if counter == len(byteKey):
                counter = 0
        return bytes(output_data)