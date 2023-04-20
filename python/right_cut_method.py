from data import FbgData
from matplotlib import pyplot as plt
from algorithms import algorithm_sprintz


NOISE_LEVEL = 2500
MAX_SAMPLE_VALUE = 10000
DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"

fbg_data = FbgData(DATA_FILES_FOLDER, 5000)
data = fbg_data.get_data_with_index(round(fbg_data.get_number_of_files() / 2))
data_denoised = list(data).copy()
for i in range(len(data_denoised)):
    if data_denoised[i] < NOISE_LEVEL:
        data_denoised[i] = NOISE_LEVEL

data_denoised = data_denoised[:(len(data_denoised) - (len(data_denoised) % 32))]
bits = algorithm_sprintz(data_denoised)
print(f"sprintz bits: {bits}")

fig, axs = plt.subplots(1)
axs.plot(data)
axs.plot(data_denoised)
axs.set_title("Example oscillogram")
axs.grid(True)
axs.set_ylim([0, MAX_SAMPLE_VALUE])
plt.show()


