from math import floor, log2
from coders.bitstream import bitstream_write, bitstream_read


def bitpacking_encode(data, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    if min(data) < 0:
        raise Exception("Negative data in input is invalid!")

    if len(data) % samples_in_packet != 0:
        raise Exception(f"Data length ({len(data)}) is not multiple of SAMPLES IN PACKET constant ({samples_in_packet})")

    samples_counter = 0
    stream = []
    bits = 0
    i = 0
    zero_packet_counter = 0

    while i < len(data):
        if samples_counter % samples_in_packet == 0:
            found_something_else_then_zero = False
            for val in data[i:i+samples_in_packet]:
                if val != 0:
                    found_something_else_then_zero = True
                    break

            if found_something_else_then_zero:
                bits = floor(log2(max(data[i:i+samples_in_packet])) + 1)
            else:
                zero_counter = 0
                for val in data[i:]:
                    if val == 0:
                        zero_counter += 1
                    else:
                        break
                zero_packets = zero_counter // samples_in_packet
                if zero_packets > 4:
                    bitstream_write(stream, 31, save_bitwidth_bits)
                    bitstream_write(stream, zero_packets, 15)
                    i += zero_packets * samples_in_packet
                    continue
                bits = 0

            if bits > max_bitwidth:
                raise Exception(f"Input data bitwidth is bigger than {max_bitwidth}")

            bitstream_write(stream, bits, save_bitwidth_bits)

        bitstream_write(stream, data[i], bits)
        samples_counter += 1
        i += 1

    return stream


def bitpacking_decode(stream, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    output = []
    while len(stream) > 0:
        bits = bitstream_read(stream, save_bitwidth_bits)

        if bits == 31:
            zero_packets = bitstream_read(stream, 15)
            for _ in range(zero_packets):
                for _ in range(samples_in_packet):
                    output.append(0)
            continue

        if bits > max_bitwidth:
            raise Exception(f"Invalid bits value: {bits}, it is bigger than max bitwidth: {max_bitwidth}")

        if bits > 0:
            for _ in range(samples_in_packet):
                output.append(bitstream_read(stream, bits))
        else:
            for _ in range(samples_in_packet):
                output.append(0)

    return output
