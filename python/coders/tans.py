from coders.bitstream import bitstream_write, bitstream_read_from_behind

CODING_SYMBOLS = 8
TABLE_SIZE = 16
TABLE_BUILDING_COEFF = 10
STATE_BITS = 8


class Tans:
    def __init__(self, occurrence):
        self.occurrence = occurrence
        self.offset, self.output_state, self.symbol_map = createCodingTable(self.occurrence)

    def get_output_state(self, symbol, input_state):
        idx = self.offset[symbol] + input_state - self.occurrence[symbol]
        return self.output_state[idx]

    def get_idx_from_state(self, state):
        idx = 0
        while idx < TABLE_SIZE:
            if self.output_state[idx] == state:
                return idx - 1
            idx += 1
        assert False

    def encode(self, data: list) -> list:
        stream = []
        state = TABLE_SIZE
        for i, symbol in enumerate(data):
            state_max = (self.occurrence[symbol] << 1) - 1
            while state > state_max:
                bitstream_write(stream, state & 1, 1)
                state >>= 1
            state = self.get_output_state(symbol, state)

        bitstream_write(stream, state, STATE_BITS)
        return stream

    def decode(self, stream: list) -> list:
        state = bitstream_read_from_behind(stream, STATE_BITS)
        bits = len(stream)
        data = []
        state_min = TABLE_SIZE
        while bits > 0:
            table_idx = self.get_idx_from_state(state)
            symbol = self.symbol_map[table_idx]
            data.append(symbol)
            state = table_idx - self.offset[symbol] + self.occurrence[symbol]
            while state < state_min:
                val = bitstream_read_from_behind(stream, 1)
                bits -= 1
                state <<= 1
                state += val

        data.reverse()
        return data


def createCodingTable(occurrence: list):
    current_state = 0
    current_output_state = TABLE_SIZE
    offset = []
    output_state = [0] * TABLE_SIZE

    offset.append(0)
    for x in occurrence[:-1]:
        offset.append(offset[-1] + x)

    for _ in range(0, TABLE_SIZE):
        output_state[current_state] = current_output_state
        current_output_state += 1
        current_state = (current_state + TABLE_BUILDING_COEFF + 3) % TABLE_SIZE

    occ_counter = 0
    act_symbol = 0
    symbol_map = [0] * TABLE_SIZE
    for i in range(TABLE_SIZE):
        symbol_map[i] = act_symbol
        occ_counter += 1
        if occ_counter == occurrence[act_symbol]:
            act_symbol += 1
            occ_counter = 0

    return offset, output_state, symbol_map
