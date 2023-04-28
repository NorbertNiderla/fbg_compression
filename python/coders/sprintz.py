from numpy import diff, cumsum

from coders.bitpacking import bitpacking_encode, bitpacking_decode
from coders.bitstream import bitstream_write, bitstream_read
from coders.fire import Fire
from coders.zigzag import zigzag_encode, zigzag_decode

MAX_BITWIDTH = 16
SAVE_BITS_WIDTH = 5


def sprintz_encode(data: list, fire_state: Fire, samples_in_packet: int) -> list:
    diff_data = fire_state.encode(data)
    normalized_data = zigzag_encode(diff_data)
    first_sample = []
    bitstream_write(first_sample, normalized_data[0], 32)
    stream = bitpacking_encode(normalized_data[1:], MAX_BITWIDTH, SAVE_BITS_WIDTH, samples_in_packet)
    stream.insert(0, first_sample[0])
    return stream


def sprintz_decode(stream: list, fire_state: Fire, samples_in_packet: int) -> list:
    first_sample = bitstream_read(stream, 32)
    normalized_data = bitpacking_decode(stream, MAX_BITWIDTH, SAVE_BITS_WIDTH, samples_in_packet)
    normalized_data.insert(0, first_sample)
    diff_data = zigzag_decode(normalized_data)
    data = fire_state.decode(diff_data)
    return data


def sprintz_diff_encode(data: list, samples_in_packet: int) -> list:
    diff_data = diff(data).tolist()
    diff_data.insert(0, data[0])
    normalized_data = zigzag_encode(diff_data)
    first_sample = []
    bitstream_write(first_sample, normalized_data[0], 32)
    stream = bitpacking_encode(normalized_data[1:], MAX_BITWIDTH, SAVE_BITS_WIDTH, samples_in_packet)
    stream.insert(0, first_sample[0])
    return stream


def sprintz_diff_decode(stream: list, samples_in_packet: int) -> list:
    first_sample = bitstream_read(stream, 32)
    normalized_data = bitpacking_decode(stream, MAX_BITWIDTH, SAVE_BITS_WIDTH, samples_in_packet)
    normalized_data.insert(0, first_sample)
    diff_data = zigzag_decode(normalized_data)
    data = cumsum(diff_data).tolist()
    return data
