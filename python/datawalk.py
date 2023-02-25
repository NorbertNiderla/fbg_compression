from matplotlib import plot as plt
from data import FbgData

DATA_FILES_FOLDER = "C:/Users/norbert/PycharmProjects/data"
fbg_data = FbgData(DATA_FILES_FOLDER, 3000)
x = list(range(0, 6180))
y = list(range(0, 6180))
plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)
plt.xlabel("Normalized Lambda")
plt.ylabel("Normalized Power")
ax.set_ylim([0, 16384])

last_file = False
while last_file is False:
    new_y, last_file = fbg_data.get_data()
    line1.set_xdata(x)
    line1.set_ydata(new_y)
    figure.canvas.draw()
    figure.canvas.flush_events()
