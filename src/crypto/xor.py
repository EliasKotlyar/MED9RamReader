# Some common passwords are BiWbBuD101, GEHEIM, CodeRobert, MILKYWAY

MED9_XOR_KEY = "RobertCode"


def xor_encrypt(data: bytes, key: str) -> bytes:
    byteKey = key.encode("ascii")
    output_data = bytearray()
    counter = 0
    for data_byte in data:
        currentXor = byteKey[counter]
        output_data.append(data_byte ^ currentXor)
        counter += 1
        if counter == len(byteKey):
            counter = 0
    return bytes(output_data)


def encrypt(data: bytes, key: str):
    dsg_key_bytes = key.encode("ascii")
    counter = 0
    offset = 0
    rolling_stream_offset = 0
    last_data = 0
    output_data = []
    while counter < len(data):
        data_byte = data[counter]
        match_index = dsg_key_bytes.index(data_byte)
        cipher_data = match_index - offset & 0xFF
        offset += data_byte
        offset += last_data
        rolling_stream_offset += 0x167
        offset += dsg_key_bytes[(rolling_stream_offset >> 8) & 0xFF]
        last_data = data_byte
        output_data.append(cipher_data)
        counter += 1
    return bytes(output_data)
