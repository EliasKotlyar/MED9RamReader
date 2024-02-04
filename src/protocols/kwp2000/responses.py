from bitstring import BitArray


class KwpResponse:
    def __init__(self, data: bytearray):
        self.data = data


class IDENT_9B_Response(KwpResponse):
    def __init__(self, data: bytearray):
        super().__init__(data)
        self.vw_part_nr = data[0:12].decode('ascii', errors='ignore')
        self.datenstand = data[15:17].decode('ascii', errors='ignore')
        byte13_bits = BitArray(bytes=data[13:14])
        self.can_be_programmed = byte13_bits[7]  # Check bit7
        self.program_stand = bytes(byte13_bits[0:6].int) + data[14:15]
        self.program_stand = self.program_stand.decode('ascii', errors='ignore')

        byte17_bits = BitArray(bytes=data[17:18])
        self.number_of_coding_table = byte17_bits[:4].int
        self.length_of_coding = byte17_bits[4:].int
        self.code1 = hex(data[18])
        self.code2 = hex(data[19])
        self.code3 = hex(data[20])
        # Workshop ID handling using bitstring
        workshop_id_bits = BitArray(bytes=data[21:26])

        # Device Number
        device_number_bits = workshop_id_bits[0:32]
        self.device_number = device_number_bits.uint

        # Importer Number
        importer_number_bits = workshop_id_bits[32:33] + workshop_id_bits[40:48]
        self.importer_number = importer_number_bits.uint

        # Operation Number
        operation_number_bits = workshop_id_bits[24:32] + workshop_id_bits[33:40]
        self.operation_number = operation_number_bits.uint
        self.misc = data[27:46]

    def __str__(self):
        return (
            f"IDENT_9B_Response:\n"
            f"  vw_part_nr: {self.vw_part_nr}\n"
            f"  datenstand: {self.datenstand}\n"
            f"  can_be_programmed: {self.can_be_programmed}\n"
            f"  program_stand: {self.program_stand}\n"
            f"  number_of_coding_table: {self.number_of_coding_table}\n"
            f"  length_of_coding: {self.length_of_coding}\n"
            f"  code1: {self.code1}\n"
            f"  code2: {self.code2}\n"
            f"  code3: {self.code3}\n"
            f"  device_number: {self.device_number}\n"
            f"  importer_number: {self.importer_number}\n"
            f"  operation_number: {self.operation_number}\n"
            f"  misc: {self.misc}"
        )


class IDENT_9C_Response(KwpResponse):
    def __init__(self, data: bytearray):
        super().__init__(data)
        bits_program_status = BitArray(uint=data[1], length=8)
        self.no_error = bool(bits_program_status[0])
        self.flash_not_programmable = bool(bits_program_status[1])
        self.communication_error = bool(bits_program_status[2])
        self.flash_not_eraseable = bool(bits_program_status[3])
        self.eeprom_faulty = bool(bits_program_status[4])
        self.inconsistency_bit = bool(bits_program_status[7])

        self.counter_programtry = int(data[1])
        self.counter_sucessfulprogram = int(data[2])
        self.preprogramming_status = BitArray(uint=data[3], length=8).bin

    def __str__(self):
        return (
            "IDENT_9C_Response:\n"
            f"    no_error: {self.no_error}\n"
            f"    flash_not_programmable: {self.flash_not_programmable}\n"
            f"    communication_error: {self.communication_error}\n"
            f"    flash_not_eraseable: {self.flash_not_eraseable}\n"
            f"    eeprom_faulty: {self.eeprom_faulty}\n"
            f"    inconsistency_bit: {self.inconsistency_bit}\n"
            f"    counter_programtry: {self.counter_programtry}\n"
            f"    counter_sucessfulprogram: {self.counter_sucessfulprogram}\n"
            f"    preprogramming_status: {self.preprogramming_status}\n"
        )


class REQUEST_SEED_RESPONSE(KwpResponse):
    def __init__(self, data: bytearray):
        super().__init__(data)
        self.seed = BitArray(bytes=data[2:6], length=32).int

    def __str__(self):
        return (
            "REQUEST_SEED_RESPONSE:\n"
            f"    seed: {hex(self.seed)}\n"
        )
