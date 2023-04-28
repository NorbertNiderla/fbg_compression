from time import time
from sympy import ceiling
from tqdm import tqdm
from Common.fbg_compression_results import FbgCompressionResults
from Common.data import FbgData
from denoise_data import denoise_data

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
PEAK_DETECTION_BASIC_THRESHOLD = 1.1
DECIMATION_RATE = 10
NOISE_LEVEL_FACTOR = 1.2
PARALEL_STREAMS = 5
FILE_STEP = 2000


def main():
    print("Fbg Compression")
    print(f"\tData folder: {DATA_FILES_FOLDER}")

    results = FbgCompressionResults()
    file_step = FILE_STEP
    dense_file_step = int(ceiling(file_step / 30))
    fbg_data = FbgData(DATA_FILES_FOLDER, file_step)
    fbg_data_dense = FbgData(DATA_FILES_FOLDER, dense_file_step)
    n_f = fbg_data.get_number_of_files()

    print("Processing parallel data")
    for x in tqdm(range(PARALEL_STREAMS)):
        noiseless_data_raw = [0] * n_f
        data_raw = [0] * n_f
        for i in range(n_f):
            data, last_file = fbg_data.get_data()
            data_noiseless = [int(round(x)) for x in denoise_data(data)]
            noiseless_data_raw[i] = data_noiseless[x]
            data_raw[i] = data[x]

        results.process_parallel_raw(data_raw)

        data_raw = [int(round(x)) for x in denoise_data(data_raw)]
        data_raw = data_raw[:(len(data_raw) - (len(data_raw) % 32))]
        results.result_raw_parallel_noiseless.process(data_raw)

        noiseless_data_raw = noiseless_data_raw[:(len(noiseless_data_raw) - (len(noiseless_data_raw) % 32))]
        results.result_noiseless_parallel.process(noiseless_data_raw)

    print("Processing normal fbg data...")
    for i in tqdm(range(n_f)):
        data = fbg_data.get_data_with_index(i)
        results.process_raw(data)
        results.process_noise_floor(data)
        results.process_decimation(data)
        results.process_noiseless(data)

    results.process_peaks_stream(fbg_data_dense)

    results.print_results()


if __name__ == "__main__":
    start_time = time()
    main()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time}")
