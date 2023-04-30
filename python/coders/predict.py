from math import log

from numpy import diff, cumsum, sign


class DeltaForecaster:
    def encode(self, data: list) -> list:
        output = diff(data).tolist()
        output.insert(0, data[0])
        return output

    def decode(self, data: list) -> list:
        return cumsum(data).tolist()


class Fire:
    def __init__(self, learning_rate=2, bitwidth=12):
        self.learning_rate = learning_rate
        self.learn_shift = int(log(self.learning_rate, 2))
        self.bitwidth = bitwidth
        self.acc = 0
        self.delta = 0

    def encode(self, data: list) -> list:
        prev_x = 0
        output = []

        for sample in data:
            x = self._predict(prev_x)
            err = sample - x
            self._train(prev_x, sample, err)
            prev_x = sample
            output.append(err)

        return output

    def decode(self, data: list) -> list:
        prev_x = 0
        output = []

        for sample in data:
            x = self._predict(prev_x)
            err = sample
            val = err + x
            self._train(prev_x, val, err)
            prev_x = val
            output.append(val)

        return output

    def _train(self, prev_x: int, x: int, err: int):
        gradient = -sign(err) * self.delta
        self.acc -= gradient
        self.delta = x - prev_x

    def _predict(self, x: int):
        alpha = self.acc >> self.learn_shift
        change = (alpha * self.delta) >> self.bitwidth
        return x + change
