from numpy import convolve, ones
from matplotlib import pyplot as plt
from Common.data import FbgData, DataFromJulek

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"


def denoise_data(data: list, step: int):
    denoised_data = convolve(data, ones(step) / step, mode='valid').tolist()
    first_sample = denoised_data[0]
    last_sample = denoised_data[-1]
    samples_to_put_in_front = (len(data) - len(denoised_data)) // 2
    samples_to_put_in_back = len(data) - len(denoised_data) - samples_to_put_in_front
    for _ in range(samples_to_put_in_front):
        denoised_data.insert(0, first_sample)
    for _ in range(samples_to_put_in_back):
        denoised_data.append(last_sample)
    return denoised_data


def main():
    # fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
    fbg_data = DataFromJulek(1000)
    data = fbg_data.get_sample_with_index(fbg_data.get_number_of_samples() // 2)

    denoised_data = denoise_data(data, 7)
    plt.plot(data, label="data")
    plt.plot(denoised_data, label="denoised data")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
