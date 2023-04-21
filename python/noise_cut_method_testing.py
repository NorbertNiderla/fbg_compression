from numpy import average
from statistics import median
from data import FbgData
from matplotlib import pyplot as plt
from algorithms import algorithm_sprintz


NOISE_LEVEL_FACTOR = 1.2
MAX_SAMPLE_VALUE = 10000
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"

fbg_data = FbgData(DATA_FILES_FOLDER, 1000)

last_file = False
number_of_files = fbg_data.get_number_of_files()
bits_all = [0]*number_of_files
bits_index = 0

while last_file is False:
    print(f"{bits_index}/{number_of_files}")
    data, last_file = fbg_data.get_data()
    noise_level = int(median(data) * NOISE_LEVEL_FACTOR)
    for i in range(len(data)):
        if data[i] < noise_level:
            data[i] = noise_level

    data = data[:(len(data) - (len(data) % 32))]
    bits_all[bits_index] = algorithm_sprintz(data)
    bits_index += 1

print(average(bits_all))

fig, axs = plt.subplots(1)
axs.plot(bits_all)
axs.set_title("Bits per sample")
axs.grid(True)
plt.show()

