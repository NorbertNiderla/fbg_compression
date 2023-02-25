from scipy.stats import entropy
from sympy import ceiling
from tqdm import tqdm
from data import FbgData
from numpy import unique, nan, average
from peak_detection import peak_detection_max, peak_detection_band
from coders.sprintz import sprintz_encode, sprintz_decode
from coders.fire import Fire
from coders.bitstream import bitstream_get_bits
from algorithms import algorithm_sprintz
from denoise_data import denoise_data


DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
MAX_SAMPLE_VALUE = 16384 - 1
PEAK_DETECTION_BASIC_THRESHOLD = 1.1
CONFIG = {
    "algorithms": {
        "Sprintz": {
            "use": True,
            "function": algorithm_sprintz,
        }
    },
    "input": {
        "raw": True,
        "noiseless": True,
        "peaks": {
            "stream": True,
            "xy": False
        }
    }
}


def main():
    print("Fbg Compression")
    print(f"\tData folder: {DATA_FILES_FOLDER}")

    file_step = 3000
    dense_file_step = int(ceiling(file_step / 30))

    fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
    fbg_data_dense = FbgData(DATA_FILES_FOLDER, dense_file_step)

    n_f = fbg_data.get_number_of_files()
    entropy_raw = [0] * n_f
    entropy_noiseless = [0] * n_f
    entropy_peaks_stream = 0
    bits_raw = {key: [0] * n_f for key, value in CONFIG["algorithms"].items() if value["use"] is True}
    bits_noiseless = {key: [0] * n_f for key, value in CONFIG["algorithms"].items() if value["use"] is True}
    bits_peak_stream = {key: 0 for key, value in CONFIG["algorithms"].items() if value["use"] is True}

    print("Processing normal fbg data...")
    for i in tqdm(range(n_f)):
        data, last_file = fbg_data.get_data()

        if CONFIG["input"]["raw"] is True:
            data_raw = data[:(len(data) - (len(data) % 32))]
            entropy_raw[i] = entropy_my(MAX_SAMPLE_VALUE, data_raw)
            for key, value in CONFIG["algorithms"].items():
                if value["use"] is True:
                    bits_raw[key][i] = value["function"](data_raw)

        if CONFIG["input"]["noiseless"] is True:
            data_noiseless = [int(round(x)) for x in denoise_data(data)]
            data_noiseless = data_noiseless[:(len(data_noiseless) - (len(data_noiseless) % 32))]
            entropy_noiseless[i] = entropy_my(MAX_SAMPLE_VALUE, data_noiseless)
            for key, value in CONFIG["algorithms"].items():
                if value["use"] is True:
                    bits_noiseless[key][i] = value["function"](data_noiseless)

    print("Calculating peaks from dense fbg data...")
    n_f = fbg_data_dense.get_number_of_files()
    peaks_band_method = [0] * n_f
    for i in tqdm(range(n_f)):
        data, last_file = fbg_data_dense.get_data()
        if CONFIG["input"]["peaks"]["stream"] is True:
            peaks_band_method[i] = peak_detection_band(data)

    print("Processing peak data...")
    number_of_peaks_in_stream = 0
    if CONFIG["input"]["peaks"]["stream"] is True:
        peaks_stream_x, peaks_stream_y = convert_peaks_into_stream(peaks_band_method)
        scale = 2 ** 12 - 1
        peaks_stream = [round(val * scale) for val in peaks_stream_y]
        peaks_stream = peaks_stream[:len(peaks_stream) - len(peaks_stream) % 32]
        for key, value in CONFIG["algorithms"].items():
            if value["use"] is True:
                bits_peak_stream[key] = value["function"](peaks_stream)
        number_of_peaks_in_stream = len(peaks_stream)
        entropy_peaks_stream = entropy_my(scale, peaks_stream)
    original_bitwidth = 14

    print("Results:")
    # Printing data from raw data processing
    if CONFIG["input"]["raw"] is True:
        print("\tRaw data lossless compression:")
        print(f"\t\tOriginal bitwidth: {original_bitwidth}")
        print(f"\t\tData entropy: {average(entropy_raw)}")
        print("\t\tBits per sample in compressed stream:")
        for key, value in CONFIG["algorithms"].items():
            if value["use"] is True:
                print(f"\t\t\t{key}: {average(bits_raw[key])}")

    # Printing data from denoised data processing
    if CONFIG["input"]["noiseless"] is True:
        print("\tDenoised data lossless compression:")
        print(f"\t\tOriginal bitwidth: {original_bitwidth}")
        print(f"\t\tData entropy: {average(entropy_noiseless)}")
        print(f"\t\tBits per sample in compressed stream:")
        for key, value in CONFIG["algorithms"].items():
            if value["use"] is True:
                print(f"\t\t\t{key}: {average(bits_noiseless[key])}")

    # Printing data from peaks stream processing
    original_bitwidth = 12
    if CONFIG["input"]["peaks"]["stream"] is True:
        print("\tPeak stream lossless compression:")
        print(f"\t\tNumber of peaks in peaks stream: {number_of_peaks_in_stream}")
        print(f"\t\tOriginal bitwidth: {original_bitwidth}")
        print(f"\t\tPeak stream entropy: {entropy_peaks_stream}")
        print(f"\t\tBits per sample in compressed stream:")
        for key, value in CONFIG["algorithms"].items():
            if value["use"] is True:
                print(f"\t\t\t{key}: {bits_peak_stream[key]}")

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
    print(f"\tNumber of peaks detected per oscillogram: {len(peak_band_all_xy[0]) / fbg_data_source.get_number_of_files()}")
    print(f"\tNumber of peaks in peaks stream: {len(peaks_stream_x)}")
    print(f"\tNumber of peaks in peaks stream per oscillogram: {len(peaks_stream_x) / fbg_data_source.get_number_of_files()}")

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
