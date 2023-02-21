import unittest
from Fire import Fire
from ZigZag import zigzagEncode, zigzagDecode
from Bitstream import writeToBitstream, readFromBitstream
from Bitpacking import bitpackingEncode, bitpackingDecode
from Sprintz import sprintzEncode, sprintzDecode


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("../data/short_sinus_data.txt") as file:
            data = [int(x) for x in file.readlines()[0:128]]
            limit = len(data)
            for x in range(limit):
                data.append(int(data[x] * 2))
            cls.data = data

    def testFire(self):
        data = [x + 300 for x in self.data]
        predictor = Fire(8, -1)
        predicted_samples = predictor.encode(data)
        predictor_decoder = Fire(8, -1)
        decoded_samples = predictor_decoder.decode(predicted_samples)
        self.assertListEqual(data, decoded_samples)

    def testZigzag(self):
        data = [x - 100 for x in self.data]
        encoded_data = zigzagEncode(data)
        decoded_data = zigzagDecode(encoded_data)
        self.assertListEqual(data, decoded_data)

    def testBitstream(self):
        stream = []
        writeToBitstream(stream, self.data[0], 10)
        writeToBitstream(stream, self.data[1], 10)
        writeToBitstream(stream, self.data[2], 10)
        values = []
        for _ in range(3):
            values.append(readFromBitstream(stream, 10))

        self.assertListEqual(self.data[0:3], values)

    def testBitpacking(self):
        max_bitwidth = 16
        save_bits_width = 6
        samples_in_packet = 8
        data = [x for x in range(256)]
        compressed_data = bitpackingEncode(data, max_bitwidth, save_bits_width, samples_in_packet)
        decompressed_data = bitpackingDecode(compressed_data, max_bitwidth, save_bits_width, samples_in_packet)
        self.assertListEqual(data, decompressed_data)
        # TODO write tests that will change input parameters to bitpacking and check whether some exceptions will arise

    def testSprintz(self):
        data = [x + 100 for x in self.data]
        predictor = Fire(8, -1)
        predictor_decom = Fire(8, -1)
        compressed_data = sprintzEncode(data, predictor)
        decompressed_data = sprintzDecode(compressed_data, predictor_decom)
        self.assertListEqual(data, decompressed_data)


if __name__ == '__main__':
    unittest.main()
