import unittest

from coders.bitstream import bitstream_write, bitstream_read_from_behind


class MyTestCase(unittest.TestCase):
    def test_bitstream_read_from_behind_basic(self):
        stream = []
        bitstream_write(stream, 1, 1)
        bitstream_write(stream, 0, 1)
        bitstream_write(stream, 21, 5)

        val1 = bitstream_read_from_behind(stream, 5)
        val2 = bitstream_read_from_behind(stream, 1)
        val3 = bitstream_read_from_behind(stream, 1)

        self.assertEqual(val1, 21)  # add assertion here
        self.assertEqual(val2, 0)
        self.assertEqual(val3, 1)


if __name__ == '__main__':
    unittest.main()
