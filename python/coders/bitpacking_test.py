import unittest
from random import randint
from coders.bitpacking import bitpacking_encode, bitpacking_decode


class MyTestCase(unittest.TestCase):
    def test_normal_bitpacking(self):
        data = [randint(0, 256) for _ in range(1024)]
        stream = bitpacking_encode(data, 16, 5, 32)
        decoded_data = bitpacking_decode(stream, 16, 5, 32)
        self.assertListEqual(data, decoded_data)

    def test_bitpacking_not_aligned_size_small(self):
        data = [0, 1, 2, 3, 4, 5, 6]
        stream = bitpacking_encode(data, 3, 3, 2)
        decoded_data = bitpacking_decode(stream, 3, 3, 2)
        self.assertListEqual(data, decoded_data)

    def test_bitpacking_random_size(self):
        data = [randint(0, 256) for _ in range(7777)]
        stream = bitpacking_encode(data, 16, 5, 32)
        decoded_data = bitpacking_decode(stream, 16, 5, 32)
        self.assertListEqual(data, decoded_data)


if __name__ == '__main__':
    unittest.main()
