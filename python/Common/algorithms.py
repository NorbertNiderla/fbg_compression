from coders.arithmetic import ArithmeticCoder
from coders.predict import Fire
from coders.sprintz import sprintz_encode, sprintz_decode, sprintz_delta_encode, sprintz_delta_decode
from coders.bitstream import bitstream_get_bits


def algorithm_sprintz_delta(data: list) -> float:
    compressed_data = sprintz_delta_encode(data, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_delta_decode(compressed_data, 32)

    if data != decompressed_data:
        print(data)
        raise ValueError("SprintzDelta coder failed!")

    return bits


def algorithm_sprintz(data: list) -> float:
    compressor_fire = Fire()
    decompressor_fire = Fire()
    compressed_data = sprintz_encode(data, compressor_fire, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_decode(compressed_data, decompressor_fire, 32)

    if data != decompressed_data:
        print(data)
        raise ValueError("Sprintz coder failed!")

    return bits


def algorithm_arithmetic(data: list) -> float:
    counts = [0] * (max(data) + 1)
    for x in data:
        counts[x] += 1

    coder = ArithmeticCoder()
    stream = coder.encode(data, counts)
    stream_len = len(stream)
    decoded_data = coder.decode(stream, counts, len(data))

    if data != decoded_data:
        print(data)
        raise ValueError("Arithmetic coder failed!")

    return stream_len / len(data)
