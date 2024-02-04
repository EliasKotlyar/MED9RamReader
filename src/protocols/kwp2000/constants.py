from enum import IntEnum
from typing import NamedTuple


class SERVICE_TYPE(IntEnum):
    ECU_RESET = 0x11
    READ_FREEZE_FRAME_DATA = 0x12
    READ_DIAGNOSTIC_TROUBLE_CODES = 0x13
    CLEAR_DIAGNOSTIC_INFORMATION = 0x14
    READ_STATUS_OF_DIAGNOSTIC_TROUBLE_CODES = 0x17
    READ_DIAGNOSITC_TROUBE_CODES_BY_STATUS = 0x18
    READ_ECU_IDENTIFICATION = 0x1A
    START_DIAGNOSTIC_SESSION = 0x10
    STOP_DIAGNOSTIC_SESSION = 0x20
    READ_DATA_BY_LOCAL_IDENTIFIER = 0x21
    READ_DATA_BY_COMMON_IDENTIFIER = 0x22
    READ_MEMORY_BY_ADDRESS = 0x23
    SET_DATA_RATES = 0x26
    SECURITY_ACCESS = 0x27
    DYNAMICALLY_DEFINE_LOCAL_IDENTIFIER = 0x2C
    WRITE_DATA_BY_COMMON_IDENTIFIER = 0x2E
    INPUT_OUTPUT_CONTROL_BY_COMMON_IDENTIFIER = 0x2F
    INPUT_OUTPUT_CONTROL_BY_LOCAL_IDENTIFIER = 0x30
    START_ROUTINE_BY_LOCAL_IDENTIFIER = 0x31
    STOP_ROUTINE_BY_LOCAL_IDENTIFIER = 0x32
    REQUEST_ROUTINE_RESULTS_BY_LOCAL_IDENTIFIER = 0x33
    REQUEST_DOWNLOAD = 0x34
    REQUEST_UPLOAD = 0x35
    TRANSFER_DATA = 0x36
    REQUEST_TRANSFER_EXIT = 0x37
    START_ROUTINE_BY_ADDRESS = 0x38
    STOP_ROUTINE_BY_ADDRESS = 0x39
    REQUEST_ROUTINE_RESULTS_BY_ADDRESS = 0x3A

    WRITE_DATA_BY_LOCAL_IDENTIFIER = 0x3B
    WRITE_MEMORY_BY_ADDRESS = 0x3D
    TESTER_PRESENT = 0x3E
    ESC_CODE = 0x80
    STOP_COMMUNICATION = 0x82


class ROUTINE_CONTROL_TYPE(IntEnum):
    ERASE_FLASH = 0xC4
    UNKNOWN = 0xB8
    CALCULATE_FLASH_CHECKSUM = 0xC5


class ECU_IDENTIFICATION_TYPE(IntEnum):
    ECU_IDENT = 0x9B
    STATUS_FLASH = 0x9C
    HW_NUMBER = 0x91
    HW_NUMBER2 = 0x86


# Taken from https://nissanecu.miraheze.org/wiki/Communication_Protocols
class SESSION_TYPE(IntEnum):
    OBD2_MODE = 0x81
    ENDOFLINE_MODE = 0x83
    PROGRAMMING = 0x85
    ENGINEERING_MODE = 0x86
    DIAGNOSTIC = 0x89
    EXTENDED_DIAG = 0x92


class ACCESS_TYPE(IntEnum):
    PROGRAMMING_REQUEST_SEED = 1
    PROGRAMMING_SEND_KEY = 2
    REQUEST_SEED = 3
    SEND_KEY = 4


class COMPRESSION_TYPE(IntEnum):
    UNCOMPRESSED = 0x0
    COMPRESSION_1 = 0x01


class ENCRYPTION_TYPE(IntEnum):
    UNENCRYPTED = 0x0
    ENCRYPTION_1 = 0x01


class DYNAMIC_DEFINITION_TYPE(IntEnum):
    DEFINE_BY_LOCAL_IDENTIFIER = 1
    DEFINE_BY_COMMON_IDENTIFIER = 2
    DEFINE_BY_MEMORY_ADDRESS = 3
    CLEAR_DYNAMICALLY_DEFINED_DATA_IDENTIFIER = 4


class DynamicSourceDefinition(NamedTuple):
    data_identifier: int
    position: int
    memory_size: int
    memory_address: int


negative_response_codes = {
    0x00: "positiveResponse",
    0x01: "ISOSAEReserved",
    0x10: "generalReject",
    0x11: "serviceNotSupported",
    0x12: "subFunctionNotSupported",
    0x13: "incorrectMessageLengthOrInvalidFormat",
    0x14: "responseTooLong",
    0x21: "busyRepeatRequest",
    0x22: "conditionsNotCorrect",
    0x23: "routineNotComplete",
    0x24: "requestSequenceError",
    0x31: "requestOutOfRange",
    0x33: "securityAccessDenied",
    0x35: "invalidKey",
    0x36: "exceedNumberOfAttempts",
    0x37: "requiredTimeDelayNotExpired",
    0x38: "reservedByExtendedDataLinkSecurityDocument",
    0x40: "downloadNotAccepted",
    0x41: "improperDownloadType",
    0x42: "cantDownloadToSpecifiedAddress",
    0x43: "cantDownloadNumberOfBytesRequested",
    0x50: "uploadNotAccepted",
    0x51: "improperUploadType",
    0x52: "cantUploadFromSpecifiedAddress",
    0x53: "cantUploadNumberOfBytesRequested",
    0x71: "transferSuspended",
    0x72: "transferAborted",
    0x74: "illegalAddressInBlockTransfer",
    0x75: "illegalByteCountInBlockTransfer",
    0x76: "illegalBlockTransferType",
    0x77: "blockTransferDataChecksumError",
    0x78: "requestCorrectlyReceived_ResponsePending",
    0x79: "incorrectByteCountDuringBlockTransfer",
    0x7E: "subFunctionNotSupportedInActiveSession",
    0x7F: "serviceNotSupportedInActiveSession",
    0x80: "ISOSAEReserved",
    0x81: "rpmTooHigh",
    0x82: "rpmTooLow",
    0x83: "engineIsRunning",
    0x84: "engineIsNotRunning",
    0x85: "engineRunTimeTooLow",
    0x86: "temperatureTooHigh",
    0x87: "temperatureTooLow",
    0x88: "vehicleSpeedTooHigh",
    0x89: "vehicleSpeedTooLow",
    0x8A: "throttle_PedalTooHigh",
    0x8B: "throttle_PedalTooLow",
    0x8C: "transmissionRangeNotInNeutral",
    0x8D: "transmissionRangeNotInGear",
    0x8F: "brakeSwitchesNotClosed",
    0x90: "shifterLeverNotInPark",
    0x91: "torqueConverterClutchLocked",
    0x92: "voltageTooHigh",
    0x93: "voltageTooLow",
    0x94: "reservedForSpecificConditionsNotCorrect",
    0xFF: "ISOSAEReserved",
    0x9A: "dataDecompressionFailed",
    0x9B: "dataDecryptionFailed",
    0xA0: "EcuNotResponding",
    0xA1: "EcuAddressUnknown"
}
