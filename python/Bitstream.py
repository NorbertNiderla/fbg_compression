def writeToBitstream(stream: list, value: int, bits: int):
    if value < 0:
        raise Exception("Value cannot be negative!")

    if bits < 1:
        raise Exception("Bits cannot be lower than 1!")

    value = value & ((1 << bits) - 1)
    stream.append(format(value, f"0{bits}b"))


def readFromBitstream(stream: list, bits: int) -> int:
    if bits < 1:
        raise Exception("Bits cannot be lower than 1!")

    value = None
    while bits > 0 and len(stream) > 0:
        value = 0
        next_len = len(stream[0])
        if bits >= next_len:
            value <<= next_len
            bits -= next_len
            value += int(stream.pop(0), 2)
        else:
            value <<= bits
            value += int(stream[0][0:bits], 2)
            stream[0] = stream[0][bits:]
            bits = 0

    return value