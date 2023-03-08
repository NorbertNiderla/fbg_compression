from coders.fire import Fire
from coders.sprintz import sprintz_encode, sprintz_decode
from coders.bitstream import bitstream_get_bits


def algorithm_sprintz(data):
    fire_learn_shift = -1
    fire_bitwidth = 16
    compressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    decompressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    compressed_data = sprintz_encode(data, compressor_fire, 32)
    bits = bitstream_get_bits(compressed_data) / len(data)
    decompressed_data = sprintz_decode(compressed_data, decompressor_fire, 32)
    if data != decompressed_data:
        raise ValueError("Sprintz coder failed!")

    return bits


# data is list of 8 frames from bragg monitor data
# n of fire coders must be the same as frame length from bragg monitor data
def algorithm_sprintz_time_along(data, fire_coders):
    frame_len = len(fire_coders)
    for i, fire in enumerate(fire_coders):
        data_batch = [0] * 8
        for x in range(8):
            data_batch[x] = data[x][i]

        # in data_batch now we have 8 consecutive samples from one wavelength


