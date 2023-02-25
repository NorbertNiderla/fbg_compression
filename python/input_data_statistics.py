from data import FbgData
from peak_detection import peak_detection_max, peak_detection_band
from fbg_compression import entropy_my, convert_None_to_NaN, convert_peaks_into_xy
from numpy import convolve, ones, average
from matplotlib import plot as plt

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
MAX_SAMPLE_VALUE = 16384 - 1
PEAK_DETECTION_BASIC_THRESHOLD = 1.1


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

    fig, axs = plt.subplots(5)
    fig.suptitle('Input data statistics')

    a = 0
    axs[a].plot(entropy_arr)
    axs[a].set_title("Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    a += 1

    axs[a].plot(moving_average_entropy_arr)
    axs[a].set_title("Moving Average Entropy")
    axs[a].grid(True)
    axs[a].set_ylim([2, 8])
    a += 1

    axs[a].plot(peak_max_arr, "bo")
    axs[a].set_title("Peak Detection (Basic Method)")
    axs[a].grid(True)
    axs[a].set_ylim([0, 1])
    a += 1

    axs[a].plot(peak_band_arr_x, peak_band_arr_y, "bo")
    axs[a].set_title("Peak Detection (Band Method)")
    axs[a].grid(True)
    axs[a].set_ylim([0, 1])
    a += 1

    axs[a].plot(fbg_data_source.get_data_with_index(round(fbg_data_source.get_number_of_files() / 2)))
    axs[a].set_title("Example oscillogram")
    axs[a].grid(True)
    axs[a].set_ylim([0, MAX_SAMPLE_VALUE])
    a += 1


if __name__ == "__main__":
    fbg_data = FbgData(DATA_FILES_FOLDER, 500)
    show_statistics(fbg_data)
    show_average_figure(fbg_data)
    plt.show()
