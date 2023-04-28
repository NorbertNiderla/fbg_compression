from numpy import ndarray

from coders.fire import Fire
from coders.sprintz import sprintz_encode, sprintz_decode, sprintz_diff_encode, sprintz_diff_decode
from coders.bitstream import bitstream_get_bits


def algorithm_sprintz_diff(data: list) -> float:
    compressed_data = sprintz_diff_encode(data, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_diff_decode(compressed_data, 32)

    if data != decompressed_data:
        raise ValueError("Sprintz coder failed!")

    return bits


def algorithm_sprintz(data: list) -> float:
    fire_learn_shift = -1
    fire_bitwidth = 32
    compressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    decompressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    compressed_data = sprintz_encode(data, compressor_fire, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_decode(compressed_data, decompressor_fire, 32)

    if data != decompressed_data:
        raise ValueError("Sprintz coder failed!")

    return bits
