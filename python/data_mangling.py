import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy
from tqdm import tqdm
from scipy.ndimage import uniform_filter1d

BM_DATA_DIR = "C:/Users/norbert/PycharmProjects/data"


def entropy1(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    return entropy(counts, base=base)


files = os.listdir(BM_DATA_DIR)
files = files[:round(len(files)*0.3)]


def data_mangling_entropy():
    c = 0.13

    with open(os.path.join(BM_DATA_DIR, files[round(len(files) * c)])) as datafile:
        a = eval(datafile.read())
        data = a["data"]
        print(entropy1(data))
        print(entropy1(np.diff(data)))


def data_mangling_peak_presence():
    all_avg = []
    print(len(files))
    for x in tqdm(range(0, len(files), 10)):
        with open(os.path.join(BM_DATA_DIR, files[x])) as datafile:
            a = eval(datafile.read())
            data = a["data"]
            all_avg.append(np.average(data))

    plt.plot(all_avg)
    plt.show()


def data_mangling_moving_average():
    with open(os.path.join(BM_DATA_DIR, files[round(len(files)*0.35)])) as datafile:
        a = eval(datafile.read())
        data = a["data"]
        avg_data = np.convolve(data, np.ones(100)/100, mode='valid').tolist()
        for _ in range(50):
            avg_data.insert(0, 2000)
        # plt.plot(data, label="data")
        # plt.plot(avg_data, label="avg")
        plt.hist(np.diff(avg_data), bins=50, log=True)
        plt.show()


if __name__ == "__main__":
    # data_mangling_peak_presence()
    data_mangling_moving_average()
