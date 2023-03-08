from numpy import convolve, ones
from data import FbgData
from matplotlib import pyplot as plt
from statistics import variance
from numpy import diff


DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"


def denoise_data(data):
    denoised_data = convolve(data, ones(30) / 30, mode='valid').tolist()
    first_sample = denoised_data[0]
    last_sample = denoised_data[-1]
    samples_to_put_in_front = round((len(data) - len(denoised_data)) / 2)
    samples_to_put_in_back = len(data) - len(denoised_data) - samples_to_put_in_front
    for _ in range(samples_to_put_in_front):
        denoised_data.insert(0, first_sample)
    for _ in range(samples_to_put_in_back):
        denoised_data.append(last_sample)
    return denoised_data


def main():
    fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
    data = fbg_data.get_data_with_index(round(fbg_data.get_number_of_files() / 2))
    denoised_data = denoise_data(data)
    plt.plot(data, label="data")
    plt.plot(denoised_data, label="denoised data")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

