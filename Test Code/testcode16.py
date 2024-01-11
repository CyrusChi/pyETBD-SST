# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 18:22:11 2023

@author: Cyrus
"""
import numpy as np
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()

x = np.linspace(-10, 10, 1000)
y = np.sin(x)

plt.plot(x, y)

ax = plt.gca()
ax.text(0.5, 1.100, "y=sin(x)", bbox={'facecolor': 'red',
                                       'alpha': 0.5, 'pad': 5},
         transform=ax.transAxes, ha="center")

def animate(frame):
   ax.text(0.5, 1.100, "y=sin(x), frame: %d" % frame,
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 5},
            transform=ax.transAxes, ha="center")

ani = animation.FuncAnimation(fig, animate, interval=100,
                              frames=10, repeat=True)

plt.show()