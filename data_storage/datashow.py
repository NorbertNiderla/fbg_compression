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
for filename in os.listdir(os.getcwd()):
    print(filename)
    i=(i+1)%1000
    if(i!=0):
        continue
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        a = eval(f.read())
        new_y = a["data"]
    
        # updating data values
        line1.set_xdata(x)
        line1.set_ydata(new_y)
    
        # drawing updated values
        figure.canvas.draw()
    
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()
    
        #time.sleep(0.1)