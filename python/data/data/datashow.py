import os
import matplotlib.pyplot as plt
import time

import numpy as np
 
# creating initial data values
# of x and y
x = list(range(0,6180))
y = list(range(0,6180))
 
# to run GUI event loop
plt.ion()
 
# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, y)
 
# setting title
plt.title("Geeks For Geeks", fontsize=20)
 
# setting x-axis label and y-axis label
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
i=0
directory = os.path.join(os.getcwd(), "data")

for filename in os.listdir(directory):
    # print(filename)
    i=(i+1)%1000
    if(i!=0):
        continue
    with open(os.path.join(directory, filename), 'r') as f:
        a = eval(f.read())
        new_y = a["data"]
        line1.set_xdata(x)
        line1.set_ydata(new_y)
        figure.canvas.draw()
        figure.canvas.flush_events()
    
        #time.sleep(0.1)
