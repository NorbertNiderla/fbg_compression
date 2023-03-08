from data import FbgData
from peak_detection import peak_detection_max, peak_detection_band
from fbg_compression import entropy_my, convert_None_to_NaN, convert_peaks_into_xy
from numpy import convolve, ones, average
from matplotlib import pyplot as plt
from statistics import variance
from numpy import diff

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
MAX_SAMPLE_VALUE = 16384 - 1
PEAK_DETECTION_BASIC_THRESHOLD = 1.1


def show_raw_figure(fbg_data_source: FbgData):
    fig, axs = plt.subplots(1)
    fig.suptitle('Raw Data')
    data = fbg_data_source.get_data_with_index(round(fbg_data_source.get_number_of_files() / 2))
    print(f"Variance of raw data: {variance(diff(data), 0)}")
    axs.plot(data)
    axs.set_title("Example oscillogram")
    axs.grid(True)
    axs.set_ylim([0, MAX_SAMPLE_VALUE])


def show_average_figure(fbg_data_source: FbgData):
    average_arr = [0] * fbg_data_source.get_number_of_files()
    last_file = False
    x = 0
    while last_file is False:
        data, last_file = fbg_data_source.get_data()
        average_arr[x] = average(data)
        x += 1
    fig, axs = plt.subplots(1)
    fig.suptitle('Data')
    axs.plot(average_arr)
    axs.set_title("Average Value")
    axs.grid(True)


def show_statistics(fbg_data_source: FbgData):
    entropy_arr = [0] * fbg_data_source.get_number_of_files()
    moving_average_entropy_arr = [0] * fbg_data_source.get_number_of_files()
    peak_max_arr = [0] * fbg_data_source.get_number_of_files()
    peak_band_arr = [0] * fbg_data_source.get_number_of_files()
    last_file = False
    x = 0

    while last_file is False:
        data, last_file = fbg_data_source.get_data()

        entropy_arr[x] = entropy_my(MAX_SAMPLE_VALUE, data)
        avg_data = convolve(data, ones(100) / 100, mode='valid').tolist()
        moving_average_entropy_arr[x] = entropy_my(MAX_SAMPLE_VALUE, avg_data)
        peak_max_arr[x] = peak_detection_max(data, PEAK_DETECTION_BASIC_THRESHOLD)
        peak_band_arr[x] = peak_detection_band(data)

        x += 1

    peak_max_arr = convert_None_to_NaN(peak_max_arr)
    peak_band_arr_x, peak_band_arr_y = convert_peaks_into_xy(peak_band_arr)

    fig, axs = plt.subplots(2)
    fig.suptitle('Input data entropy')

    a = 0
    axs[a].plot(entropy_arr)
    axs[a].set_title("Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    plt.xlabel("Frame number")
    plt.ylabel("Set entropy")

    a += 1

    axs[a].plot(moving_average_entropy_arr)
    axs[a].set_title("Moving Average Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    # axs[a].xlabel("Frame number")
    # axs[a].ylabel("Set entropy")


    a = 0

    fig2, axs2 = plt.subplots(2)
    fig2.suptitle('Peak detection')
    axs2[a].plot(peak_max_arr, "bo")
    axs2[a].set_title("Peak Detection (Basic Method)")
    axs2[a].grid(True)
    axs2[a].set_ylim([0, 1])
    # axs[a].ylabel("Normalized wavelength")
    # axs[a].xlabel("Frame number")
    a += 1

    axs2[a].plot(peak_band_arr_x, peak_band_arr_y, "bo")
    axs2[a].set_title("Peak Detection (Band Method)")
    axs2[a].grid(True)
    axs2[a].set_ylim([0, 1])
    # axs[a].ylabel("Normalized wavelength")
    # axs[a].xlabel("Frame number")
    a += 1


if __name__ == "__main__":
    fbg_data = FbgData(DATA_FILES_FOLDER, 500)
    show_statistics(fbg_data)
    show_raw_figure(fbg_data)
    show_average_figure(fbg_data)
    plt.show()
