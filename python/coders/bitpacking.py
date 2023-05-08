from math import floor, log2
from coders.bitstream import bitstream_write, bitstream_read

RLE_SYMBOL = 31
RLE_BITWIDTH = 15


def count_leading_symbols(arr: list, symbol: int) -> int:
    counter = 0
    for x in arr:
        if x == symbol:
            counter += 1
        else:
            break
    return counter


def append_symbol(arr: list, symbol: int, n: int):
    for _ in range(n):
        arr.append(symbol)


def bitpacking_encode(data, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    if min(data) < 0:
        raise Exception("Negative data in input is invalid!")

    stream = []
    bits = 0
    i = 0
    samples_in_packet_counter = 0

    while i < len(data):
        if samples_in_packet_counter == 0:
            if all(element == 0 for element in data[i:(i + samples_in_packet)]):
                bits = 0
                zero_counter = count_leading_symbols(data[i:], 0)
                if zero_counter // samples_in_packet > 4:
                    bitstream_write(stream, RLE_SYMBOL, save_bitwidth_bits)
                    bitstream_write(stream, zero_counter, RLE_BITWIDTH)
                    i += zero_counter
                    continue
            else:
                bits = floor(log2(max(data[i:i + samples_in_packet])) + 1)

            if bits > max_bitwidth:
                raise Exception(f"Input data bitwidth is bigger than {max_bitwidth}")

            if i + samples_in_packet > len(data) and bits == 0:
                bits = 1

            bitstream_write(stream, bits, save_bitwidth_bits)

        bitstream_write(stream, data[i], bits)
        i += 1
        samples_in_packet_counter += 1

        if samples_in_packet_counter == samples_in_packet:
            samples_in_packet_counter = 0

    return stream


def bitpacking_decode(stream, max_bitwidth, save_bitwidth_bits, samples_in_packet):
    output = []
    while len(stream) > 0:
        bits = bitstream_read(stream, save_bitwidth_bits)

        if bits == RLE_SYMBOL:
            zero_counter = bitstream_read(stream, RLE_BITWIDTH)
            append_symbol(output, 0, zero_counter)
            continue

        if bits > max_bitwidth:
            raise Exception(f"Invalid bits value: {bits}, it is bigger than max bitwidth: {max_bitwidth}")

        if bits > 0:
            for _ in range(samples_in_packet):
                if len(stream) == 0:
                    break
                output.append(bitstream_read(stream, bits))
        else:
            append_symbol(output, 0, samples_in_packet)

    return output
