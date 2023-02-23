class Fire:
    def __init__(self, bitwidth, learn_shift):
        self.learn_shift = learn_shift
        self.bitwidth = bitwidth
        self.accumulator = 0
        self.delta = 0
        self.last_sample = 0

    def predict(self, sample):
        if self.learn_shift > 0:
            alpha = self.accumulator >> self.learn_shift
        elif self.learn_shift < 0:
            alpha = self.accumulator << -self.learn_shift
        else:
            alpha = self.accumulator

        if self.delta >= 0:
            return sample + ((alpha * self.delta) >> self.bitwidth)
        else:
            return sample - ((-alpha * self.delta) >> self.bitwidth)

    def train(self, sample, sample_next, error):
        if error >= 0:
            self.accumulator += self.delta
        else:
            self.accumulator -= self.delta

        if self.accumulator < 0:
            self.accumulator = 0

        self.delta = sample_next - sample

    def encode(self, data: list) -> list:
        temp = self.predict(self.last_sample)
        self.train(self.last_sample, data[0], data[0] - temp)
        self.last_sample = data[-1]
        output = []
        for idx, sample in enumerate(data[:-1]):
            output.append(temp - sample)
            temp = self.predict(sample)
            self.train(sample, data[idx + 1], data[idx + 1] - temp)

        output.append(temp - data[-1])
        return output

    def decode(self, data):
        temp = self.predict(self.last_sample)
        self.train(self.last_sample, temp - data[0], -data[0])
        output = []
        for idx, sample in enumerate(data[:-1]):
            output.append(temp - sample)
            temp = self.predict(output[-1])
            self.train(output[-1], temp - data[idx + 1], -data[idx + 1])

        output.append(temp - data[-1])
        self.last_sample = output[-1]
        return output


if __name__ == "__main__":
    raise Exception("This file should not be invoked directly!")
