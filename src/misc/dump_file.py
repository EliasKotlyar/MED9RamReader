from src.misc.binarydump import BinaryDump


def read_dump_file(inputfile: str) -> BinaryDump:
    '''
    Reads the content of a binary file and returns a BinaryDump object.

    Parameters:
    - inputfile (str): The path to the binary file.

    Returns:
    - BinaryDump: An instance of BinaryDump containing the content of the binary file.

    Raises:
    - FileNotFoundError: If the specified input file does not exist.
    '''
    # Method for reading the input file.
    # It takes the input file path as input and returns the file content.
    try:
        with open(inputfile, 'rb') as input_file:
            content = input_file.read()
            return BinaryDump(content)

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Input file '{inputfile}' does not exist.")


def write_dump_file(outputfile: str, dump: BinaryDump):
    """
    Writes the provided binary content to a binary file.

    Parameters:
    - outputfile (str): The name or path of the output binary file.
    - content (bytearray): The binary content to write to the file.

    Returns:
    - None
    """
    content = dump.get_bytes()
    with open(outputfile, "wb") as file:
        file.write(content)
