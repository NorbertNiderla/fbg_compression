from statistics import mean
import numpy as np
from numpy import ndarray
from scipy.fft import dct, idct
from matplotlib import pyplot as plt
from Common.data import DataFromJulek, FbgData


def mse(arr1: ndarray, arr2: ndarray) -> float:
    return mean([(x - y) ** 2 for x, y in zip(arr1, arr2)])


def dct_test_core(data: list, compression_ratio: float) -> float:
    time_series = np.array(data)
    dct_coefficients = dct(time_series, norm='ortho')
    threshold = np.percentile(np.abs(dct_coefficients), (1 - compression_ratio) * 100)
    dct_coefficients_compressed = np.where(np.abs(dct_coefficients) >= threshold, dct_coefficients, 0)
    time_series_reconstructed = idct(dct_coefficients_compressed, norm='ortho')
    return mse(time_series, time_series_reconstructed) / len(time_series)


def dct_processed(data: list, compression_ratio: float) -> list:
    time_series = np.array(data)
    dct_coefficients = dct(time_series, norm='ortho')
    threshold = np.percentile(np.abs(dct_coefficients), (1 - compression_ratio) * 100)
    dct_coefficients_compressed = np.where(np.abs(dct_coefficients) >= threshold, dct_coefficients, 0)
    time_series_reconstructed = list(idct(dct_coefficients_compressed, norm='ortho'))
    return time_series_reconstructed


def dct_test(data: list, compression_ratios: list) -> list:
    errors = []
    for ratio in compression_ratios:
        errors.append(dct_test_core(data, ratio))
    return errors


def main():
    fbg_data_julek = DataFromJulek(1000)
    fbg_data = FbgData("C:/Users/norbert/PycharmProjects/data", 10000)
    data = fbg_data.get_sample_with_index(fbg_data.get_number_of_samples() // 2)
    data_julek = fbg_data_julek.get_sample_with_index(fbg_data_julek.get_number_of_samples() // 2)

    ratios_julek = list(np.logspace(np.log10(0.8), np.log10(0.01), 20))
    ratios = list(np.logspace(np.log10(0.5), np.log10(0.01), 20))

    errors = dct_test(data, ratios)
    errors_julek = dct_test(data_julek, ratios_julek)

    fig, axs = plt.subplots(1, 1)
    axs.scatter([16 * x for x in ratios_julek], errors_julek, label="Wąski zbiór danych")
    axs.scatter([16 * x for x in ratios], errors, label="Szeroki zbiór danych")
    axs.set_xlabel('Średnia szerokość bitowa')
    axs.set_ylabel('Błąd MSE')
    axs.set_title('Kompresja DCT')
    axs.grid(True)
    axs.legend()
    axs.set_yscale("log")
    # plt.ylim([0, max(errors_julek) + 10])
    plt.savefig("Figures/mse_dct.pdf", bbox_inches='tight', format="pdf")

    fig, axs = plt.subplots(1, 1)
    axs.plot(data, label="Dane oryginalne")
    axs.plot(dct_processed(data, 0.025), label="Dane po dekompresji")
    axs.set_xlabel('Numer próbki')
    axs.set_ylabel('Znormalizowana moc optyczna')
    axs.set_title('Kompresja DCT - zbiór szeroki')
    axs.grid(True)
    axs.legend()
    plt.savefig("Figures/dct_wide_example.pdf", bbox_inches='tight', format="pdf")

    fig, axs = plt.subplots(1, 1)
    axs.plot(data_julek, label="Dane oryginalne")
    axs.plot(dct_processed(data_julek, 0.25), label="Dane po dekompresji")
    axs.set_xlabel('Numer próbki')
    axs.set_ylabel('Znormalizowana moc optyczna')
    axs.set_title('Kompresja DCT - zbiór wąski')
    axs.grid(True)
    axs.legend()
    plt.savefig("Figures/dct_thin_example.pdf", bbox_inches='tight', format="pdf")


if __name__ == "__main__":
    main()
