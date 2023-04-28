from statistics import median
from Common.algorithms import algorithm_sprintz, algorithm_sprintz_diff
from data.parse_od_julka import get_data_from_julek

x, y = get_data_from_julek()
bits_all = [0]

for data in y:
    noise_level = int(median(data) * 1.2)
    data_noise_floor = data.copy()
    for x in range(len(data_noise_floor)):
        if data_noise_floor[x] < noise_level:
            data_noise_floor[x] = noise_level

    data_noise_floor = data_noise_floor[:(len(data_noise_floor) - (len(data_noise_floor) % 32) - 31)]

    data_noise_floor = data_noise_floor.tolist()
    bits = algorithm_sprintz_diff(data_noise_floor)
    bits_all.append(bits)

print(sum(bits_all) / len(bits_all))
