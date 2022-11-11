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
            data = file.read(-1).replace("'","\"").replace("\n", "")
            temperature_string = data[data.find("temperature"):]
            all_temperature.append(int(temperature_string.split()[1][:-1]))
            all_samples.append(data.split("(")[1].split(")")[0].split(", "))

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
                


def main():
    # data_files_path = join(getcwd(), join("data", "bm_data"))
    # filenames = listdir(data_files_path)
    # with open(file=join(data_files_path, filenames[0]), mode="r", encoding = "utf-8") as file:
    #     data = file.read().replace("'","\"").replace("\n", "").replace("(", "[").replace(")", "]")
        

    # data = read_samples_from_bm_data()
    # samples = {"samples":data[0], "temp":data[1]}
    # with open(file=join(getcwd(), join("data", "bm_samples.txt")), mode="w", encoding="utf-8") as file:
    #     dump(samples, file)

    # samples = read_samples_from_bm_samples()

    # plot.hist(samples["samples"], log=True)

    #odstep pomiedzy tymi dziwnymi wypustkami w dół to jest 6180 probek
    #dlugosc czasu ktora jest zapisana w plikach to w tym momencie jest 123-16=107 sekund
    #ilosc probek w plikach w tym momencie wynosi: 3250680
    #co po przeliczeniu daje około 30kSa, zatem dziwna wypustka występuję z częstotliwością 5Hz

    # data = array_split(samples["samples"], 500)
    # plot.subplot(2,1,1)
    # plot.plot([mean(x) for x in data])
    # plot.subplot(2,1,2)
    # plot.plot(samples["temp"])
    # plot.plot(samples["samples"])
    # plot.show()
    
    save_data_to_binary_file()


if __name__ == "__main__":
    main()
