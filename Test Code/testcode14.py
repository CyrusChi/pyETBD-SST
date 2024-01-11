# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:14:36 2023

@author: Cyrus
"""
import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import animation

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import figure

# plt.rcParams['animation.ffmpeg_path'] = '/opt/local/bin/ffmpeg'
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\Cyrus\Documents\Python_stuff\ffmpeg-2023-03-30-git-4d216654ca-full_build\bin\ffmpeg.exe'
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)


FFwriter = animation.FFMpegWriter(fps=5,extra_args=['-s', '600x500'])
# FFwriter = animation.FFMpegWriter(fps=30,extra_args=['-vf', "pad=ceil(iw/2)*2:ceil(ih/2)*2"])
# FFwriter = animation.FFMpegWriter(fps=30)
anim.save('basic_animation.mp4', writer=FFwriter)

#f = r"C:\Users\Cyrus\Downloads\animation_mp4.mp4" 
#writervideo = animation.FFMpegWriter(fps=30, extra_args=['-vcodec', 'libx264'])
#anim.save(f, writer=writervideo)