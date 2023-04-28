from math import floor, log2
from coders.bitstream import bitstream_write, bitstream_read


def bitpacking_encode(data, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    if min(data) < 0:
        raise Exception("Negative data in input is invalid!")

    samples_counter = 0
    stream = []
    bits = 0

    for i in range(len(data)):
        if i % samples_in_packet == 0:
            if all(element == 0 for element in data[i:(i+samples_in_packet)]):
                bits = 0
            else:
                bits = floor(log2(max(data[i:i+samples_in_packet])) + 1)

            if bits > max_bitwidth:
                raise Exception(f"Input data bitwidth is bigger than {max_bitwidth}")

            if i + samples_in_packet > len(data) and bits == 0:
                bits = 1

            bitstream_write(stream, bits, save_bitwidth_bits)

        bitstream_write(stream, data[i], bits)
        samples_counter += 1

    return stream


def bitpacking_decode(stream, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    output = []
    while len(stream) > 0:
        bits = bitstream_read(stream, save_bitwidth_bits)

        if bits > max_bitwidth:
            raise Exception(f"Invalid bits value: {bits}, it is bigger than max bitwidth: {max_bitwidth}")

        if bits > 0:
            for _ in range(samples_in_packet):
                if len(stream) == 0:
                    break
                output.append(bitstream_read(stream, bits))
        else:
            for _ in range(samples_in_packet):
                output.append(0)

    return output
