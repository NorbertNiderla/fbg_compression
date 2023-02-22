from matplotlib import pyplot as plt
from scipy.stats import entropy
from data import FbgData
from numpy import convolve, ones, unique, nan, average
from peak_detection import peak_detection_max, peak_detection_band
from enum import Enum


class ProgramType(Enum):
    DATAWALK = 0
    AVERAGE_VALUE = 1
    STATISTICS = 2


PROGRAM_TYPE = ProgramType.STATISTICS
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
MAX_SAMPLE_VALUE = 16384 - 1
PEAK_DETECTION_BASIC_THRESHOLD = 1.1
FILE_STEP = 1000


def main():
    print("Fbg Compression")
    print(f"Data folder: {DATA_FILES_FOLDER}")
    fbg_data = FbgData(DATA_FILES_FOLDER, FILE_STEP)
    if PROGRAM_TYPE == ProgramType.STATISTICS:
        show_statistics(fbg_data)
    elif PROGRAM_TYPE == ProgramType.DATAWALK:
        show_datawalk(fbg_data)
    elif PROGRAM_TYPE == PROGRAM_TYPE.AVERAGE_VALUE:
        show_average_figure(fbg_data)


def show_average_figure(fbg_data_source: FbgData):
    average_arr = [0] * fbg_data_source.get_number_of_files()
    last_file = False
    x = 0
    while last_file is False:
        data, last_file = fbg_data_source.get_data()
        average_arr[x] = average(data)
        x += 1
    fig, axs = plt.subplots(5)
    fig.suptitle('Data')
    axs[0].plot(average_arr)
    axs[0].set_title("Average Value")
    axs[0].grid(True)


def show_statistics(fbg_data_source: FbgData):
    entropy_arr = [0] * fbg_data_source.get_number_of_files()
    moving_average_entropy_arr = [0] * fbg_data_source.get_number_of_files()
    peak_max_arr = [0] * fbg_data_source.get_number_of_files()
    peak_band_arr = [0] * fbg_data_source.get_number_of_files()
    last_file = False
    x = 0

    while last_file is False:
        data, last_file = fbg_data_source.get_data()

        entropy_arr[x] = entropy_my(MAX_SAMPLE_VALUE, data)
        avg_data = convolve(data, ones(100) / 100, mode='valid').tolist()
        moving_average_entropy_arr[x] = entropy_my(MAX_SAMPLE_VALUE, avg_data)
        peak_max_arr[x] = peak_detection_max(data, PEAK_DETECTION_BASIC_THRESHOLD)
        peak_band_arr[x] = peak_detection_band(data)

        x += 1

    peak_max_arr = convert_None_to_NaN(peak_max_arr)
    peak_band_arr = turn_list_of_lists(peak_band_arr)

    fig, axs = plt.subplots(4)
    fig.suptitle('Data')

    a = 0
    axs[a].plot(entropy_arr)
    axs[a].set_title("Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    a += 1

    axs[a].plot(moving_average_entropy_arr)
    axs[a].set_title("Moving Average Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    a += 1

    axs[a].plot(peak_max_arr, "bo")
    axs[a].set_title("Peak Detection (Basic Method)")
    axs[a].grid(True)
    axs[a].set_ylim([0, 1])
    a += 1

    print("Peak detection Band Method:")
    print(f"\tMaximum of individual peaks detected:{len(peak_band_arr)}")
    for small_list in peak_band_arr:
        small_list = convert_None_to_NaN(small_list)
        axs[a].plot(small_list, "bo")
    axs[a].set_title("Peak Detection (Band Method)")
    axs[a].grid(True)
    axs[a].set_ylim([0, 1])

    plt.show()


def show_datawalk(fbg_data_source: FbgData):
    x = list(range(0, 6180))
    y = list(range(0, 6180))
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(x, y)
    plt.xlabel("Normalized Lambda")
    plt.ylabel("Normalized Power")
    ax.set_ylim([0, 16384])

    last_file = False
    while last_file is False:
        new_y, last_file = fbg_data_source.get_data()
        line1.set_xdata(x)
        line1.set_ydata(new_y)
        figure.canvas.draw()
        figure.canvas.flush_events()
    plt.close(figure)


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


if __name__ == "__main__":
    main()
