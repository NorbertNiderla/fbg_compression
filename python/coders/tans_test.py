import unittest

from coders.tans import Tans


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data = [0, 5, 2, 4, 1, 2, 5, 1, 6, 4]
        occurrences = [1, 1, 2, 3, 5, 2, 1, 1]
        tans = Tans(occurrences)
        stream = tans.encode(data)
        decoded_data = tans.decode(stream)
        self.assertListEqual(data, decoded_data)


if __name__ == '__main__':
    unittest.main()
