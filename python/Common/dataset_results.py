from numpy import average
from Common.algorithm_result import AlgorithmResult
from Common.algorithms import algorithm_sprintz, algorithm_sprintz_delta
from Common.utility import entropy_my


class DataSetResults:
    def __init__(self, data_set_name: str, original_bitwidth: int):
        self.original_bitwidth = original_bitwidth
        self.max_value = 2 ** self.original_bitwidth - 1
        self.data_set_name = data_set_name
        self.entropy = []
        self.mse = []
        self.results = {
            "sprintz": (AlgorithmResult("sprintz"), algorithm_sprintz),
            "sprintz delta": (AlgorithmResult("sprintz delta"), algorithm_sprintz_delta)
        }

    def process(self, data):
        self.append_entropy(entropy_my(self.max_value, data))
        for r in self.results.values():
            r[0].append_bits(r[1](data))

    def append_entropy(self, val: float):
        self.entropy.append(val)

    def append_mse(self, val: float):
        self.mse.append(val)

    def print_results(self):
        print(f"\tData set: {self.data_set_name}")
        print(f"\tOriginal bitwidth: {self.original_bitwidth}")
        print(f"\tMax value: {self.max_value}")
        print(f"\tEntropy: {average(self.entropy)}")
        for r in self.results.values():
            r[0].print_results()

    def get_results(self):
        results = {
            "data set": self.data_set_name,
            "original bitwidth": self.original_bitwidth,
            "entropy": average(self.entropy),
            "mse": average(self.mse),
            "results": []
        }

        for r in self.results.values():
            results["results"].append(r[0].get_results())

        return results
