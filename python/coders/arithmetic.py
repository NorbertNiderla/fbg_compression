from math import ceil, floor
from numpy import cumsum, insert
from numpy.core.fromnumeric import searchsorted


def shift_l(value):
    return (value << 1) & 0xffffffff


def arithmetic_encode(data, counts):
    top_value = 2147483647  # 0xFFFFFFFF
    first_qtr = 536870912  # 0x40000000
    half = 1073741824  # 0x80000000
    third_qtr = 1610612736  # 0xC0000000

    high = top_value
    low = 0
    scale = 0
    out = []

    bounds = cumsum(counts, dtype=int)
    bounds = insert(bounds, 0, 0)

    for symbol in data:
        if (symbol > len(bounds) - 1) or (symbol < 0):
            raise Exception("symbol not found in counts array")

        step = high - low + 1
        high = low + (ceil(step / bounds[-1] * bounds[symbol + 1])) - 1
        low = low + (floor(step / bounds[-1] * bounds[symbol]))

        assert high != low

        while high < half or low >= half:
            if high < half:
                low = shift_l(low)
                high = shift_l(high) + 1
                out.append(0)
                while scale > 0:
                    out.append(1)
                    scale = scale - 1
            elif low >= half:
                low = shift_l(low - half)
                high = shift_l(high - half) + 1
                out.append(1)
                while scale > 0:
                    out.append(0)
                    scale = scale - 1

        while (low >= first_qtr) and (high < third_qtr):
            scale = scale + 1
            low = shift_l(low - first_qtr)
            high = shift_l(high - first_qtr) + 1

    if low < first_qtr:
        out.append(0)
        while scale >= 0:
            out.append(1)
            scale = scale - 1
    else:
        out.append(1)

    return out


def arithmetic_decode(stream, counts, target_size):
    top_value = 2147483647  # 0xFFFFFFFF
    first_qtr = 536870912  # 0x40000000
    half = 1073741824  # 0x80000000
    third_qtr = 1610612736  # 0xC0000000

    low = 0
    high = top_value
    value = 0
    idx = 0
    for _ in range(1000):
        stream.append(0)

    for _ in range(0, 31):
        value = shift_l(value) + stream[idx]
        idx = idx + 1

    out = []
    bounds = cumsum(counts, dtype=int)
    bounds = insert(bounds, 0, 0)

    for _ in range(0, target_size):
        step = high - low + 1
        cum = (value - low) / step * bounds[-1]
        symbol = searchsorted(bounds, cum) - 1

        if symbol < 0 or symbol > (len(counts) - 1):
            raise Exception(f"no symbol found: h:{high} l:{low} v:{value} c:{cum}, s:{symbol}")

        out.append(symbol)

        high = low + ceil(step / bounds[-1] * bounds[symbol + 1]) - 1
        low = low + floor(step / bounds[-1] * bounds[symbol])

        assert high != low

        while high < half or low >= half:
            if high < half:
                low = shift_l(low)
                high = shift_l(high) + 1
                value = shift_l(value) + stream[idx]
                idx = idx + 1
            elif low >= half:
                low = shift_l(low - half)
                high = shift_l(high - half) + 1
                value = shift_l(value - half) + stream[idx]
                idx = idx + 1
            if idx == len(stream):
                return out

        while low >= first_qtr and high < third_qtr:
            low = shift_l(low - first_qtr)
            high = shift_l(high - first_qtr) + 1
            value = shift_l(value - first_qtr) + stream[idx]
            idx = idx + 1
            if idx == len(stream):
                return out

    return out


def count_symbols(data_stream, number_of_symbols):
    counts = [0] * number_of_symbols
    for symbol in data_stream:
        if symbol < 0 or symbol > number_of_symbols - 1:
            raise Exception("symbol out of bounds")
        counts[symbol] = counts[symbol] + 1
    return counts


def set_counts_min_value(counts, min_value):
    for i, val in enumerate(counts):
        if val < min_value:
            counts[i] = min_value


def set_counts_in_range(counts, range_low, range_high):
    interval = range_high - range_low
    for idx, val in enumerate(counts):
        counts[idx] = floor(val / sum(counts) * interval + range_low)
