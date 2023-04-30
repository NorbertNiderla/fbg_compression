import threading
from statistics import median, mean

from tqdm import tqdm

from Common.dataset_results import DataSetResults
from Common.data import FbgData, Data
from Common.utility import convert_peaks_into_stream
from denoise_data import denoise_data
from peak_detection import peak_detection_band

DEFAULT_DECIMATION_RATE = 10
DEFAULT_NOISE_LEVEL_FACTOR = 1.2
PARALEL_STREAMS = 5


def mse(arr1: list, arr2: list) -> float:
    return mean([(x - y) ** 2 for x, y in zip(arr1, arr2)])


def threading_calculate_peak_detection_band(start: int, end: int, data_source: Data, results: list):
    for i in range(start, end):
        data = data_source.get_sample_with_index(i)
        results[i] = peak_detection_band(data)


class FbgCompressionResults:
    def __init__(self):
        self.result_raw = DataSetResults("raw", 14)
        self.result_noiseless = DataSetResults("noiseless", 14)
        self.result_peaks_stream = DataSetResults("peaks stream", 12)
        self.result_raw_parallel = DataSetResults("raw parallel", 14)
        self.result_noiseless_parallel = DataSetResults("noiseless parallel", 14)
        self.result_raw_parallel_noiseless = DataSetResults("raw parallel noiseless", 14)
        self.result_noise_floor = DataSetResults("noise floor", 14)
        self.decimation_rate = DEFAULT_DECIMATION_RATE
        self.noise_level_factor = DEFAULT_NOISE_LEVEL_FACTOR

    def add_and_process_dataset(self, data_source: Data, data_source_dense: Data):
        n_f = data_source.get_number_of_samples()

        print("Processing parallel data")
        for x in tqdm(range(PARALEL_STREAMS)):
            noiseless_data_raw = [0] * n_f
            data_raw = [0] * n_f
            for i in range(n_f):
                data = data_source.get_next_sample()
                data_noiseless = [int(round(x)) for x in denoise_data(data)]
                noiseless_data_raw[i] = data_noiseless[x]
                data_raw[i] = data[x]

            self.process_parallel_raw(data_raw)

            data_raw = [int(round(x)) for x in denoise_data(data_raw)]
            self.result_raw_parallel_noiseless.process(data_raw)
            self.result_noiseless_parallel.append_mse(mse(data_raw, noiseless_data_raw))
            self.result_raw_parallel_noiseless.append_mse(mse(data_raw, noiseless_data_raw))
            self.result_noiseless_parallel.process(noiseless_data_raw)

        print("Processing normal fbg data...")
        for i in tqdm(range(n_f)):
            data = data_source.get_sample_with_index(i)
            self.process_raw(data)
            self.process_noise_floor(data)
            self.process_noiseless(data)

        print("Processing peaks stream...")
        self.process_peaks_stream(data_source_dense)

        return self.get_results()

    def get_results(self):
        results = [self.result_raw.get_results(), self.result_noiseless.get_results(),
                   self.result_peaks_stream.get_results(), self.result_raw_parallel.get_results(),
                   self.result_noiseless_parallel.get_results(), self.result_raw_parallel_noiseless.get_results(),
                   self.result_noise_floor.get_results()]
        return results

    def process_peaks_stream(self, data: Data):
        n_f = data.get_number_of_samples()
        peaks_band_method = [0] * n_f

        num_threads = 4
        threads = []
        items_per_thread = n_f // num_threads

        for i in range(num_threads):
            start = i * items_per_thread
            if i == 3:
                end = n_f
            else:
                end = start + items_per_thread
            thread = threading.Thread(target=threading_calculate_peak_detection_band,
                                      args=(start, end, data, peaks_band_method))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        peaks_stream_x, peaks_stream_y = convert_peaks_into_stream(peaks_band_method)
        scale = 2 ** 12 - 1
        peaks_stream = [round(val * scale) for val in peaks_stream_y]
        self.result_peaks_stream.process(peaks_stream)

    def process_noise_floor(self, data: list):
        noise_level = int(median(data) * self.noise_level_factor)
        data_noise_floor = data.copy()
        for x in range(len(data_noise_floor)):
            if data_noise_floor[x] < noise_level:
                data_noise_floor[x] = noise_level

        self.result_noise_floor.append_mse(mse(data, data_noise_floor))
        self.result_noise_floor.process(data_noise_floor)

    def process_noiseless(self, data: list):
        data_noiseless = [int(round(x)) for x in denoise_data(data)]
        self.result_noiseless.append_mse(mse(data, data_noiseless))
        self.result_noiseless.process(data_noiseless)

    def process_raw(self, data: list):
        self.result_raw.process(data)

    def process_parallel_raw(self, parallel_data: list):
        self.result_raw_parallel.process(parallel_data)
