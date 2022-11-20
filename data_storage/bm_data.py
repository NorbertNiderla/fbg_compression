from os import listdir, getcwd
from os.path import join
import matplotlib.pyplot as plot
from json import dump, loads
from numpy import array_split
from statistics import mean


def read_samples_from_bm_data():
    data_files_path = join(getcwd(), join("data", "bm_data"))
    filenames = listdir(data_files_path)
    all_samples = []
    all_temperature = []
    for filename in filenames:
        with open(file=join(data_files_path, filename), mode="r", encoding = "utf-8") as file:
            data = eval(file.read())

    samples = [int(x) for batch in all_samples for x in batch]
    return samples, all_temperature

def incremental_histogram():
    data_files_path = join(getcwd(), join("data", "bm_data"))
    filenames = listdir(data_files_path)
    histogram = [0]*10000
    for filename in filenames[5000:10000]:
        with open(file=join(data_files_path, filename), mode="r", encoding = "utf-8") as file:
            data = file.read().replace("'","\"").replace("\n", "").replace("(", "[").replace(")", "]")
            data = loads(data)
            for sample in data["data"]:
                histogram[sample] += 1

    return histogram

def save_data_to_binary_file():
    data_files_path = join(getcwd(), join("data", "bm_data"))
    output_files_path = join(getcwd(), join("data", "bm_data_bin"))
    filenames = listdir(data_files_path)
    filename_counter = 0
    for filename in filenames[5000:5001]:
        with open(file=join(data_files_path, filename), mode="r", encoding = "utf-8") as file:
            data = file.read().replace("'","\"").replace("\n", "").replace("(", "[").replace(")", "]")
            data = loads(data)
            with open(file = join(output_files_path, str(filename_counter)), mode="wb") as output_file:
                samples = data["data"]
                little_endian_bytes = [[x & 0xFF, (x & 0xFF00) >> 8] for x in samples]
                little_endian_bytes = [x for sublist in little_endian_bytes for x in sublist]
                output_file.write(bytearray(little_endian_bytes))
                filename_counter += 1

def save_to_binary_file(samples, filename):
    with open(file = join(getcwd(), filename), mode="wb") as output_file:
        little_endian_bytes = [[x & 0xFF, (x & 0xFF00) >> 8] for x in samples]
        little_endian_bytes = [x for sublist in little_endian_bytes for x in sublist]
        output_file.write(bytearray(little_endian_bytes))


def main():
    data_folder = join(getcwd(), join("data", "bm_data"))
    data_output_folder = join("data", "bm_data_bin")
    filename_counter = 0
    for filename in listdir(data_folder):
        with open(join(data_folder, filename), 'r') as f:
            data = eval(f.read())
            samples = data["data"]
            save_to_binary_file(samples, join(data_output_folder, str(filename_counter)))
            filename_counter += 1


if __name__ == "__main__":
    main()
