from math import floor, log2
from Bitstream import writeToBitstream, readFromBitstream


def bitpackingEncode(data, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    if min(data) < 0:
        raise Exception("Negative data in input is invalid!")

    if len(data) % samples_in_packet != 0:
        raise Exception(f"Data length ({len(data)}) is not multiple of SAMPLES IN PACKET constant ({samples_in_packet})")

    samples_counter = 0
    stream = []
    bits = 0
    for i, sample in enumerate(data):
        if samples_counter % samples_in_packet == 0:

            found_something_else_then_zero = False;
            for val in data[i:i+samples_in_packet]:
                if val != 0:
                    found_something_else_then_zero = True
                    break

            if found_something_else_then_zero:
                bits = floor(log2(max(data[i:i+samples_in_packet])) + 1)
            else:
                bits = 0

            if bits > max_bitwidth:
                raise Exception(f"Input data bitwidth is bigger than {max_bitwidth}")

            writeToBitstream(stream, bits, save_bitwidth_bits)

        writeToBitstream(stream, sample, bits)
        samples_counter += 1

    return stream


def bitpackingDecode(stream, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    output = []
    while len(stream) > 0:
        bits = readFromBitstream(stream, save_bitwidth_bits)
        if bits > max_bitwidth:
            raise Exception(f"Invalid bits value: {bits}, it is bigger than max bitwidth: {max_bitwidth}")

        for _ in range(samples_in_packet):
            output.append(readFromBitstream(stream, bits))

    return output
