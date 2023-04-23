from math import nan
from numpy import unique
from scipy.stats import entropy


def entropy_my(max_value, labels, base=None):
    value, counts = unique(labels, return_counts=True)
    real_counts = [0] * (max_value + 1)
    for val, count in zip(value, counts):
        real_counts[int(round(val))] = count
    return entropy(real_counts, base=base)


def convert_None_to_NaN(arr):
    for i, v in enumerate(arr):
        if v is None:
            arr[i] = nan
    return arr


def turn_list_of_lists(arr):
    n_lists = max([len(x) for x in arr])
    list_of_lists = [[0] * len(arr) for x in range(n_lists)]
    for small_idx, small_list in enumerate(arr):
        for idx, val in enumerate(small_list):
            list_of_lists[idx][small_idx] = val

    return list_of_lists


def convert_peaks_into_xy(arr):
    x_plot, y_plot = [], []
    for x, y_set in enumerate(arr):
        if y_set[0] is not None:
            for y in y_set:
                x_plot.append(x)
                y_plot.append(y)

    return x_plot, y_plot


def convert_peaks_into_stream(arr):
    stream_x = []
    stream_y = []
    for x, y_set in enumerate(arr):
        if y_set[0] is not None:
            stream_y.append(min(y_set))
            stream_x.append(x)
    return stream_x, stream_y
