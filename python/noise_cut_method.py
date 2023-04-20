from data import FbgData
from matplotlib import pyplot as plt
from statistics import variance
from numpy import diff
from algorithms import algorithm_sprintz

SHIFT = 10
MAX_SAMPLE_VALUE = 10000
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"

fbg_data = FbgData(DATA_FILES_FOLDER, 5000)
data = fbg_data.get_data_with_index(round(fbg_data.get_number_of_files() / 2))
data_shifted = [x >> SHIFT for x in data]

print(f"Variance of raw data: {variance(diff(data_shifted), 0)}")

fig, axs = plt.subplots(1)
axs.plot(data)
axs.plot([x << SHIFT for x in data_shifted])
axs.set_title("Example oscillogram")
axs.grid(True)
axs.set_ylim([0, MAX_SAMPLE_VALUE])
plt.show()
