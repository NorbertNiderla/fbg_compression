from python.coders.bitpacking import bitpacking_encode, bitpacking_decode
from python.coders.fire import Fire
from python.coders.zigzag import zigzag_encode, zigzag_decode

MAX_BITWIDTH = 16
SAVE_BITS_WIDTH = 5
SAMPLES_IN_PACKET = 32


def sprintz_encode(data: list, fire_state: Fire) -> list:
    diff_data = fire_state.encode(data)
    normalized_data = zigzag_encode(diff_data)
    stream = bitpacking_encode(normalized_data, MAX_BITWIDTH, SAVE_BITS_WIDTH, SAMPLES_IN_PACKET)
    return stream


def sprintz_decode(stream: list, fire_state: Fire) -> list:
    normalized_data = bitpacking_decode(stream, MAX_BITWIDTH, SAVE_BITS_WIDTH, SAMPLES_IN_PACKET)
    diff_data = zigzag_decode(normalized_data)
    data = fire_state.decode(diff_data)
    return data


def main():
    with open("../data/short_sinus_data.txt") as file:
        data = [int(x) for x in file.readlines()[0:128]]
    limit = len(data)
    for x in range(limit):
        data.append(int(data[x] * 2 + 100))

    data = [x + 100 for x in data]
    data = data[:16]

    print(data)
    predictor = Fire(8, -1)
    predictor_decom = Fire(8, -1)
    compressed_data = sprintz_encode(data, predictor)
    decompressed_data = sprintz_decode(compressed_data, predictor_decom)
    print(decompressed_data)
    # for val in zip(data, decompressed_data):
    #     print(f"{val[0] == val[1]} {val}")


if __name__ == "__main__":
    main()
