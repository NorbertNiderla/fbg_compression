from numpy import average
from Common.algorithm_result import AlgorithmResult
from Common.algorithms import algorithm_sprintz
from Common.utility import entropy_my


class DataSetResults:
    def __init__(self, data_set_name: str, original_bitwidth: int):
        self.original_bitwidth = original_bitwidth
        self.max_value = 2 ** self.original_bitwidth - 1
        self.data_set_name = data_set_name
        self.entropy = []
        self.result_sprintz = AlgorithmResult("sprintz")

    def process(self, data):
        self.append_entropy(entropy_my(self.max_value, data))
        self.result_sprintz.append_bits(algorithm_sprintz(data))

    def append_entropy(self, val: float):
        self.entropy.append(val)

    def print_results(self):
        print(f"\tData set: {self.data_set_name}")
        print(f"\tOriginal bitwidth: {self.original_bitwidth}")
        print(f"\tMax value: {self.max_value}")
        print(f"\tEntropy: {average(self.entropy)}")
        self.result_sprintz.print_results()
