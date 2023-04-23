from statistics import median

from scipy.stats import entropy
from sympy import ceiling
from tqdm import tqdm
from data import FbgData
from numpy import unique, nan, average
from peak_detection import peak_detection_band
from algorithms import algorithm_sprintz
from denoise_data import denoise_data


DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
PEAK_DETECTION_BASIC_THRESHOLD = 1.1
DECIMATION_RATE = 10
NOISE_LEVEL_FACTOR = 1.2


class AlgorithmResult:
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.bits = []

    def append_bits(self, bits: int):
        self.bits.append(bits)

    def print_results(self):
        print(f"\t\t{self.algorithm}: {average(self.bits)}")


class DataSetResults:
    def __init__(self, data_set_name: str, original_bitwidth: int):
        self.original_bitwidth = original_bitwidth
        self.max_value = 2 ** self.original_bitwidth - 1
        self.data_set_name = data_set_name
        self.entropy = []
        self.result_sprintz = AlgorithmResult("sprintz")

    def process(self, data):
        self.append_entropy(entropy_my(self.max_value, data))
        self.result_sprintz.append_bits(algorithm_sprintz(data))

    def append_entropy(self, val: float):
        self.entropy.append(val)

    def print_results(self):
        print(f"\tData set: {self.data_set_name}")
        print(f"\tOriginal bitwidth: {self.original_bitwidth}")
        print(f"\tMax value: {self.max_value}")
        print(f"\tEntropy: {average(self.entropy)}")
        self.result_sprintz.print_results()


class Results:
    def __init__(self):
        self.result_raw = DataSetResults("raw", 14)
        self.result_noiseless = DataSetResults("noiseless", 14)
        self.result_peaks_stream = DataSetResults("peaks stream", 12)
        self.result_raw_parallel = DataSetResults("raw parallel", 14)
        self.result_noiseless_parallel = DataSetResults("noiseless parallel", 14)
        self.result_raw_parallel_noiseless = DataSetResults("raw parallel noiseless", 14)
        self.result_decimation = DataSetResults("decimation", 14)
        self.result_noise_floor = DataSetResults("noise floor", 14)

    def print_results(self):
        print("Results:")
        self.result_raw.print_results()
        self.result_noiseless.print_results()
        self.result_peaks_stream.print_results()
        self.result_raw_parallel.print_results()
        self.result_noiseless_parallel.print_results()
        self.result_raw_parallel_noiseless.print_results()
        self.result_decimation.print_results()
        self.result_noise_floor.print_results()


def main():
    print("Fbg Compression")
    print(f"\tData folder: {DATA_FILES_FOLDER}")

    results = Results()
    file_step = 200
    dense_file_step = int(ceiling(file_step / 30))
    fbg_data = FbgData(DATA_FILES_FOLDER, file_step)
    fbg_data_dense = FbgData(DATA_FILES_FOLDER, dense_file_step)
    n_f = fbg_data.get_number_of_files()

    print("Processing parallel data")
    for x in tqdm(range(15)):
        data_raw = [0] * n_f
        for i in range(n_f):
            data, last_file = fbg_data.get_data()
            data_raw[i] = data[x]

        data_raw = data_raw[:(len(data_raw) - (len(data_raw) % 32))]
        results.result_raw_parallel.process(data_raw)

    print("Processing noiseless parallel data")
    for x in tqdm(range(15)):
        noiseless_data_raw = [0] * n_f
        data_raw = [0] * n_f
        for i in range(n_f):
            data, last_file = fbg_data.get_data()
            data_noiseless = [int(round(x)) for x in denoise_data(data)]
            noiseless_data_raw[i] = data_noiseless[x]
            data_raw[i] = data[x]

        data_raw = [int(round(x)) for x in denoise_data(data_raw)]
        data_raw = data_raw[:(len(data_raw) - (len(data_raw) % 32))]
        results.result_raw_parallel_noiseless.process(data_raw)

        noiseless_data_raw = noiseless_data_raw[:(len(noiseless_data_raw) - (len(noiseless_data_raw) % 32))]
        results.result_noiseless_parallel.process(noiseless_data_raw)

    print("Processing normal fbg data...")
    for i in tqdm(range(n_f)):
        data, last_file = fbg_data.get_data()
        data_raw = data[:(len(data) - (len(data) % 32))]
        data_decimation = [x for idx, x in enumerate(data) if idx % DECIMATION_RATE == 0]
        data_decimation = data_decimation[:(len(data_decimation) - (len(data_decimation) % 32))]

        noise_level = int(median(data) * NOISE_LEVEL_FACTOR)
        data_noise_floor = data.copy()
        for i in range(len(data_noise_floor)):
            if data_noise_floor[i] < noise_level:
                data_noise_floor[i] = noise_level

        data_noise_floor = data_noise_floor[:(len(data_noise_floor) - (len(data_noise_floor) % 32))]

        results.result_noise_floor.process(data_noise_floor)
        results.result_raw.process(data_raw)
        results.result_decimation.process(data_decimation)

        data_noiseless = [int(round(x)) for x in denoise_data(data)]
        data_noiseless = data_noiseless[:(len(data_noiseless) - (len(data_noiseless) % 32))]
        results.result_noiseless.process(data_noiseless)

    print("Calculating peaks from dense fbg data...")
    n_f = fbg_data_dense.get_number_of_files()
    peaks_band_method = [0] * n_f
    for i in tqdm(range(n_f)):
        data, last_file = fbg_data_dense.get_data()
        peaks_band_method[i] = peak_detection_band(data)

    print("Processing peak data...")
    peaks_stream_x, peaks_stream_y = convert_peaks_into_stream(peaks_band_method)
    scale = 2 ** 12 - 1
    peaks_stream = [round(val * scale) for val in peaks_stream_y]
    peaks_stream = peaks_stream[:len(peaks_stream) - len(peaks_stream) % 32]
    results.result_peaks_stream.process(peaks_stream)

    results.print_results()


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


if __name__ == "__main__":
    main()
