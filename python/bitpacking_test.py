from random import randint

from coders.bitpacking import bitpacking_encode, bitpacking_decode


def test_bitpacking():
    data = [randint(0, 256) for _ in range(7777)]

    for _ in range(300):
        data.insert(2000, 0)

    for _ in range(200):
        data.append(0)

    stream = bitpacking_encode(data, 16, 5, 32)
    decoded_data = bitpacking_decode(stream, 16, 5, 32)

    assert data == decoded_data
