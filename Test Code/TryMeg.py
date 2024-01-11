# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 22:12:55 2023

@author: Cyrus
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
fig, ax = plt.subplots()
rng = np.random.default_rng(19680801)
data = np.array([20, 20, 20, 20])
x = np.array([1, 2, 3, 4])

artists = []
colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple']
for i in range(20):
    data += rng.integers(low=0, high=10, size=data.shape)
    container = ax.barh(x, data, color=colors)
    artists.append(container)



writer = animation.FFMpegWriter(fps=100,codec='mpeg4', bitrate=1000000,extra_args=["-preset", "veryslow","-crf","0","-i","pipe:.png"]); 


ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=400)
ani.save(filename="/tmp/ffmpeg_example.mp4", writer=writer)
#ani.save(filename="/tmp/ffmpeg_example.mp4", writer='imagemagick')

#plt.show()

