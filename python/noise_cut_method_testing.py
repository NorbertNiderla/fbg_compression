from numpy import average

from data import FbgData
from matplotlib import pyplot as plt
from algorithms import algorithm_sprintz


NOISE_LEVEL = 2500
MAX_SAMPLE_VALUE = 10000
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"

fbg_data = FbgData(DATA_FILES_FOLDER, 500)

last_file = False
bits_all = [0]*fbg_data.get_number_of_files()
bits_index = 0

print(f"number of files: {fbg_data.get_number_of_files()}")

while last_file is False:
    print(bits_index)
    data, last_file = fbg_data.get_data()
    for i in range(len(data)):
        if data[i] < NOISE_LEVEL:
            data[i] = NOISE_LEVEL

    data = data[:(len(data) - (len(data) % 32))]
    bits_all[bits_index] = algorithm_sprintz(data)
    bits_index += 1

print(average(bits_all))

fig, axs = plt.subplots(1)
axs.plot(bits_all)
axs.set_title("Bits per sample")
axs.grid(True)
plt.show()

