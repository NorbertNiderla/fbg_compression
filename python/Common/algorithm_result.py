from numpy import average


class AlgorithmResult:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.bits = []

    def append_bits(self, bits: int):
        self.bits.append(bits)

    def print_results(self):
        print(f"\t\t{self.algorithm}: {average(self.bits)}")