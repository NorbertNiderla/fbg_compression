from numpy import cumsum

CODE_VALUE_BITS = 32
TOP_VALUE = (1 << CODE_VALUE_BITS) - 1
FIRST_QTR = TOP_VALUE // 4 + 1
HALF = TOP_VALUE // 2 + 1
THIRD_QTR = TOP_VALUE // 4 * 3 + 1


class ArithmeticCoder:
    def __init__(self):
        self.value = None
        self.stream = None
        self.bits_to_follow = None
        self.high = None
        self.low = None

    def encode(self, data, counts) -> list:
        self.low = 0
        self.high = TOP_VALUE
        self.bits_to_follow = 0
        self.stream = []
        cum_freqs = cumsum(counts).tolist()
        cum_freqs.insert(0, 0)

        for symbol in data:
            self.encode_symbol(symbol, cum_freqs)

        self.bits_to_follow += 1
        if self.low < FIRST_QTR:
            self.bit_plus_follow(0)
        else:
            self.bit_plus_follow(1)

        return self.stream

    def decode(self, stream, counts, target_size) -> list:
        self.stream = stream
        self.value = 0
        for i in range(0, CODE_VALUE_BITS):
            if len(self.stream) > 0:
                self.value = 2 * self.value + self.stream.pop(0)
            else:
                self.value = 2 * self.value
        self.low = 0
        self.high = TOP_VALUE
        cum_freqs = cumsum(counts).tolist()
        cum_freqs.insert(0, 0)
        output = [0] * target_size

        for x in range(target_size):
            output[x] = self.decode_symbol(cum_freqs)

        return output

    def bit_plus_follow(self, bit):
        self.stream.append(bit)
        for _ in range(self.bits_to_follow):
            if bit == 0:
                self.stream.append(1)
            else:
                self.stream.append(0)
        self.bits_to_follow = 0

    def encode_symbol(self, symbol, cum_freq):
        step = self.high - self.low + 1
        self.high = self.low + (step * cum_freq[symbol + 1]) // cum_freq[-1] - 1
        self.low = self.low + (step * cum_freq[symbol]) // cum_freq[-1]

        while True:
            if self.high < HALF:
                self.bit_plus_follow(0)
            elif self.low >= HALF:
                self.bit_plus_follow(1)
                self.low -= HALF
                self.high -= HALF
            elif self.low >= FIRST_QTR and self.high < THIRD_QTR:
                self.bits_to_follow += 1
                self.low -= FIRST_QTR
                self.high -= FIRST_QTR
            else:
                break

            self.low = 2 * self.low
            self.high = (2 * self.high) + 1

    def decode_symbol(self, cum_freq):
        step = self.high - self.low + 1
        cum = ((self.value - self.low + 1) * cum_freq[-1] - 1) // step

        symbol = 0
        while not (cum_freq[symbol] <= cum < cum_freq[symbol + 1]):
            symbol += 1

        assert symbol <= len(cum_freq) - 2

        self.high = self.low + (step * cum_freq[symbol + 1]) // cum_freq[-1] - 1
        self.low = self.low + (step * cum_freq[symbol]) // cum_freq[-1]

        while True:
            if self.high < HALF:
                pass
            elif self.low >= HALF:
                self.value -= HALF
                self.low -= HALF
                self.high -= HALF
            elif self.low >= FIRST_QTR and self.high < THIRD_QTR:
                self.value -= FIRST_QTR
                self.low -= FIRST_QTR
                self.high -= FIRST_QTR
            else:
                break

            self.low = 2 * self.low
            self.high = (2 * self.high) + 1

            if len(self.stream) > 0:
                self.value = 2 * self.value + self.stream.pop(0)
            else:
                self.value = 2 * self.value

        return symbol
