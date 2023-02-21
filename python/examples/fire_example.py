from Fire import Fire
import matplotlib.pyplot as plot
from random import seed, random
import numpy

NOISE_COEFFICIENT = 50
PREDICTOR_LEARN_COEFFICIENT = -1

seed(1)

with open("../data/short_sinus_data.txt") as file:
    data = [int(x) for x in file.readlines()[0:128]]

data = [x + NOISE_COEFFICIENT*(random() - 0.5) for x in data]
data = [int(round(x)) for x in data]

plot.plot(data)

predictor = Fire(8, PREDICTOR_LEARN_COEFFICIENT)
predicted_data = numpy.cumsum([-x for x in predictor.encode(data)])
numpy.insert(predicted_data, 0, 0)


plot.plot(predicted_data)
plot.show()

