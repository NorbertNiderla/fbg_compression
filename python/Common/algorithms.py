from coders.arithmetic import arithmetic_encode, arithmetic_decode
from coders.predict import Fire
from coders.sprintz import sprintz_encode, sprintz_decode, sprintz_delta_encode, sprintz_delta_decode
from coders.bitstream import bitstream_get_bits


def algorithm_sprintz_delta(data: list) -> float:
    compressed_data = sprintz_delta_encode(data, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_delta_decode(compressed_data, 32)

    if data != decompressed_data:
        raise ValueError("SprintzDelta coder failed!")

    return bits


def algorithm_sprintz(data: list) -> float:
    compressor_fire = Fire()
    decompressor_fire = Fire()
    compressed_data = sprintz_encode(data, compressor_fire, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_decode(compressed_data, decompressor_fire, 32)

    if data != decompressed_data:
        raise ValueError("Sprintz coder failed!")

    return bits


def algorithm_arithmetic(data: list) -> float:
    base = min(data)
    counts = [0] * (max(data) - base + 1)
    for x in data:
        counts[base - x] += 1

    stream = arithmetic_encode([x - base for x in data], counts)
    decoded_data = arithmetic_decode(stream, counts, len(data))

    decoded_data = [x + base for x in decoded_data]

    if data != decoded_data:
        raise ValueError("Arithmetic coder failed!")

    return len(stream) / len(data)
