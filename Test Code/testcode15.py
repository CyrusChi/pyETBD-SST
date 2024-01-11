# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:22:10 2023

@author: Cyrus
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\Cyrus\Documents\Python_stuff\ffmpeg-2023-03-30-git-4d216654ca-full_build\bin\ffmpeg.exe'
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'

fig = plt.figure()
ax = fig.add_subplot(111)
div = make_axes_locatable(ax)
cax = div.append_axes('right', '5%', '5%')
data = np.random.rand(5, 5)
im = ax.imshow(data)
cb = fig.colorbar(im, cax=cax)
tx = ax.set_title('Frame 0')

cmap = ["copper", 'RdBu_r', 'Oranges', 'cividis', 'hot', 'plasma']

def animate(i):
   cax.cla()
   data = np.random.rand(5, 5)
   im = ax.imshow(data, cmap=cmap[i%len(cmap)])
   fig.colorbar(im, cax=cax)
   tx.set_text('Frame {0}'.format(i))

ani = animation.FuncAnimation(fig, animate, frames=10)
FFwriter = animation.FFMpegWriter()
ani.save('plot.mp4', writer=FFwriter)