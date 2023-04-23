import threading
from statistics import median

from Common.dataset_results import DataSetResults
from Common.data import FbgData
from Common.utility import convert_peaks_into_stream
from denoise_data import denoise_data
from peak_detection import peak_detection_band

DEFAULT_DECIMATION_RATE = 10
DEFAULT_NOISE_LEVEL_FACTOR = 1.2


def threading_calculate_peak_detection_band(start: int, end: int, fbg_data: FbgData, results: list):
    for i in range(start, end):
        data = fbg_data.get_data_with_index(i)
        results[i] = peak_detection_band(data)


class FbgCompressionResults:
    def __init__(self):
        self.result_raw = DataSetResults("raw", 14)
        self.result_noiseless = DataSetResults("noiseless", 14)
        self.result_peaks_stream = DataSetResults("peaks stream", 12)
        self.result_raw_parallel = DataSetResults("raw parallel", 14)
        self.result_noiseless_parallel = DataSetResults("noiseless parallel", 14)
        self.result_raw_parallel_noiseless = DataSetResults("raw parallel noiseless", 14)
        self.result_decimation = DataSetResults("decimation", 14)
        self.result_noise_floor = DataSetResults("noise floor", 14)
        self.decimation_rate = DEFAULT_DECIMATION_RATE
        self.noise_level_factor = DEFAULT_NOISE_LEVEL_FACTOR

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

    def process_decimation(self, data: list):
        data_decimation = [x for idx, x in enumerate(data) if idx % self.decimation_rate == 0]
        data_decimation = data_decimation[:(len(data_decimation) - (len(data_decimation) % 32))]
        self.result_decimation.process(data_decimation)

    def process_peaks_stream(self, data: FbgData):
        n_f = data.get_number_of_files()
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
        peaks_stream = peaks_stream[:len(peaks_stream) - len(peaks_stream) % 32]
        self.result_peaks_stream.process(peaks_stream)

    def process_noise_floor(self, data: list):
        noise_level = int(median(data) * self.noise_level_factor)
        data_noise_floor = data.copy()
        for x in range(len(data_noise_floor)):
            if data_noise_floor[x] < noise_level:
                data_noise_floor[x] = noise_level

        data_noise_floor = data_noise_floor[:(len(data_noise_floor) - (len(data_noise_floor) % 32))]

        self.result_noise_floor.process(data_noise_floor)

    def process_noiseless(self, data: list):
        data_noiseless = [int(round(x)) for x in denoise_data(data)]
        data_noiseless = data_noiseless[:(len(data_noiseless) - (len(data_noiseless) % 32))]
        self.result_noiseless.process(data_noiseless)

    def process_raw(self, data: list):
        data_raw = data[:(len(data) - (len(data) % 32))]
        self.result_raw.process(data_raw)

    def process_parallel_raw(self, parallel_data: list):
        self.result_raw_parallel.process(parallel_data[:(len(parallel_data) - (len(parallel_data) % 32))])
