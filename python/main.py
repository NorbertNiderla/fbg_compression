from time import time
from sympy import ceiling
from Common.data import FbgData, DataFromJulek
from Common.fbg_compression_results import FbgCompressionResults
from pprint import pprint

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
PEAK_DETECTION_BASIC_THRESHOLD = 1.1
DECIMATION_RATE = 10
NOISE_LEVEL_FACTOR = 1.2

# WIDE_OSCYLLOGRAM_NUM = 100
# WIDE_OSCYLLOGRAMS_DENSE_NUM = 3000
# THIN_OSCYLLOGRAM_NUM = 1000
# THIN_OSCYLLOGRAM_DENSE_NUM = 30000
WIDE_OSCYLLOGRAM_NUM = 20
WIDE_OSCYLLOGRAMS_DENSE_NUM = 600
THIN_OSCYLLOGRAM_NUM = 200
THIN_OSCYLLOGRAM_DENSE_NUM = 6000


FILE_STEP = 78500 // WIDE_OSCYLLOGRAM_NUM
DENSE_FILE_STEP = 78500 // WIDE_OSCYLLOGRAMS_DENSE_NUM
JULEK_FILE_STEP = 33138 // THIN_OSCYLLOGRAM_NUM
DENSE_JULEK_FILE_STEP = 33138 // THIN_OSCYLLOGRAM_DENSE_NUM


def main():
    fbg_compression = FbgCompressionResults()

    file_step = FILE_STEP
    dense_file_step = int(ceiling(file_step / 30))
    fbg_data = FbgData(DATA_FILES_FOLDER, file_step)
    fbg_data_dense = FbgData(DATA_FILES_FOLDER, dense_file_step)

    julek_data = DataFromJulek(JULEK_FILE_STEP)
    julek_dense_data = DataFromJulek(DENSE_JULEK_FILE_STEP)

    results = {
        "multiple peaks": fbg_compression.add_and_process_dataset(fbg_data, fbg_data_dense),
        "single peak": fbg_compression.add_and_process_dataset(julek_data, julek_dense_data)
    }

    pprint(results)


if __name__ == "__main__":
    start_time = time()
    main()
    end_time = time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time}")
