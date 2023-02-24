from matplotlib import pyplot as plt
from scipy.stats import entropy
from data import FbgData
from numpy import convolve, ones, unique, nan, average
from peak_detection import peak_detection_max, peak_detection_band
from enum import Enum
from coders.sprintz import sprintz_encode, sprintz_decode
from coders.fire import Fire
from coders.bitstream import bitstream_get_bits


class ProgramType(Enum):
    DATAWALK = 0
    AVERAGE_VALUE = 1
    INPUT_DATA_STATISTICS = 2
    LOSSLESS_COMPRESSION = 3
    PEAKS_LOSSLESS_COMPRESSION = 4


PROGRAM_TYPE = ProgramType.PEAKS_LOSSLESS_COMPRESSION
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
MAX_SAMPLE_VALUE = 16384 - 1
PEAK_DETECTION_BASIC_THRESHOLD = 1.1


def main():
    print("Fbg Compression")
    print(f"Data folder: {DATA_FILES_FOLDER}")

    if PROGRAM_TYPE == ProgramType.INPUT_DATA_STATISTICS:
        fbg_data = FbgData(DATA_FILES_FOLDER, 500)
        show_statistics(fbg_data)

    elif PROGRAM_TYPE == ProgramType.DATAWALK:
        fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
        show_datawalk(fbg_data)

    elif PROGRAM_TYPE == ProgramType.AVERAGE_VALUE:
        fbg_data = FbgData(DATA_FILES_FOLDER, 500)
        show_average_figure(fbg_data)

    elif PROGRAM_TYPE == ProgramType.LOSSLESS_COMPRESSION:
        fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
        show_lossless_compression(fbg_data)

    elif PROGRAM_TYPE == ProgramType.PEAKS_LOSSLESS_COMPRESSION:
        fbg_data = FbgData(DATA_FILES_FOLDER, 100)
        show_peaks_lossless_compression(fbg_data)


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
    peak_band_arr_x, peak_band_arr_y = convert_peaks_into_xy(peak_band_arr)

    fig, axs = plt.subplots(5)
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

    axs[a].plot(peak_band_arr_x, peak_band_arr_y, "bo")
    axs[a].set_title("Peak Detection (Band Method)")
    axs[a].grid(True)
    axs[a].set_ylim([0, 1])
    a += 1

    axs[a].plot(fbg_data_source.get_data_with_index(round(fbg_data_source.get_number_of_files() / 2)))
    axs[a].set_title("Example oscillogram")
    axs[a].grid(True)
    axs[a].set_ylim([0, MAX_SAMPLE_VALUE])
    a += 1

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


def show_lossless_compression(fbg_data_source):
    # SPRINTZ
    fire_learn_shift = -1
    fire_bitwidth = 16

    entropy_all = [0] * fbg_data_source.get_number_of_files()
    bits_all = [0] * fbg_data_source.get_number_of_files()
    i = 0
    last_file = False

    while last_file is False:
        data, last_file = fbg_data_source.get_data()
        data = data[:(len(data) - (len(data) % 32))]
        compressor_fire = Fire(fire_bitwidth, fire_learn_shift)
        decompressor_fire = Fire(fire_bitwidth, fire_learn_shift)
        compressed_data = sprintz_encode(data, compressor_fire)

        bits_all[i] = bitstream_get_bits(compressed_data) / len(data)
        entropy_all[i] = entropy_my(MAX_SAMPLE_VALUE, data)

        decompressed_data = sprintz_decode(compressed_data, decompressor_fire)

        if data != decompressed_data:
            raise ValueError("Sprintz coder failed!")

        i += 1

    original_bitwidth = 12
    print("Sprintz lossless compression:")
    print(f"\tOriginal bitwidth: {original_bitwidth}")
    print(f"\tData entropy: {average(entropy_all)}")
    print(f"\tBits per sample in compressed stream: {average(bits_all)}")

    # fig, axs = plt.subplots(1)
    # fig.suptitle('Lossless compression')
    # axs.plot(entropy_all, label="entropy")
    # axs.plot(bits_all, label="compression")
    # axs.plot([original_bitwidth for _ in range(len(bits_all))], label="original")
    # axs.set_title("Sprintz compression results")
    # axs.grid(True)
    # axs.set_ylim([0, original_bitwidth + 1])
    # plt.legend()
    # plt.show()


def get_peaks_band_method(fbg_data_source):
    last_file = False
    peak_band_all = [0] * fbg_data_source.get_number_of_files()
    x = 0

    while last_file is False:
        data, last_file = fbg_data_source.get_data()
        peak_band_all[x] = peak_detection_band(data)
        x += 1
    return peak_band_all


def show_peaks_lossless_compression(fbg_data_source):
    peak_band_all = get_peaks_band_method(fbg_data_source)
    peak_band_all_xy = convert_peaks_into_xy(peak_band_all)
    peaks_stream_x, peaks_stream_y = convert_peaks_into_stream(peak_band_all)

    print("Peaks lossless compression:")
    print(f"\tNumber of peaks detected: {len(peak_band_all_xy[0])}")
    print(
        f"\tNumber of peaks detected per oscillogram: {len(peak_band_all_xy[0]) / fbg_data_source.get_number_of_files()}")
    print(f"\tNumber of peaks in peaks stream: {len(peaks_stream_x)}")
    print(
        f"\tNumber of peaks in peaks stream per oscillogram: {len(peaks_stream_x) / fbg_data_source.get_number_of_files()}")

    # fig, axs = plt.subplots(1)
    # fig.suptitle('Peaks lossless compression')
    # axs.plot(peak_band_all_xy[0], peak_band_all_xy[1], "bo", label="peaks")
    # axs.plot(peaks_stream_x, peaks_stream_y, label="peaks stream", color="r")
    # axs.grid(True)
    # axs.set_ylim([0, 1])
    # plt.legend()
    # plt.show()

    scale = 2 ** 12 - 1
    peaks_stream = [round(val * scale) for val in peaks_stream_y]
    peaks_stream = peaks_stream[:len(peaks_stream) - len(peaks_stream) % 32]

    # sprintz
    fire_bitwidth = 16
    fire_learn_shift = -1
    compressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    decompressor_fire = Fire(fire_bitwidth, fire_learn_shift)
    compressed_data = sprintz_encode(peaks_stream, compressor_fire, 32)
    bits = bitstream_get_bits(compressed_data)
    decompressed_data = sprintz_decode(compressed_data, decompressor_fire, 32)
    if peaks_stream != decompressed_data:
        raise ValueError("Sprintz coder failed!")

    print(f"\tSprintz peaks lossless compression:")
    print(f"\t\tOriginal bitwidth: {12}")
    print(f"\t\tData entropy: {entropy_my(scale, peaks_stream)}")
    print(f"\t\tBits per sample: {bits / len(peaks_stream)}")


if __name__ == "__main__":
    main()
