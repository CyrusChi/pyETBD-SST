# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 10:49:12 2023

@author: Cyrus
"""
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import scipy.stats
import math
import pandas as pd
import glob
from pathlib import Path
import os
import sys


CI = 0.9 #confidence interval
rounded = 3
exp_name = "Exp3I-t2"
folder_name = "Exp3I-t2"
crit_name_element = "EN2_RI120_RM50_TR20K_"
subset_range = False
ss_start = 1500
ss_end = 20500

    
import_file_name = 'Exp3I-t2_TR10k_combined_CSV'
import_folder = f"{folder_name}_data_analysis" 
import_path = str(Path(f"C:/Users/Cyrus/Documents/Emory/Lab/Dissertation Explorations/Dissertation Testing - Initial Inputs and Results/{exp_name} Results/{import_folder}/"))

# 
file_list = glob.glob(f"{import_path}/*{import_file_name}*.csv")

ax = plt.figure().add_subplot(projection='3d')
filepath = f"{import_path}/{import_file_name}.csv"
# print((filepath))
try:
   temp_data = pd.read_csv(filepath)

except:
    print("raw data file not found!")  
    print(f'file list = {filepath}')
    sys.exit()


    
# print(temp_data.head())

# sys.exit()  
# Make data.
# X = np.arange(-5, 5, 0.25)
X = temp_data["RM"]
xlen = len(X)
# xlen = len(X)
# Y = np.arange(-5, 5, 0.25)
Y = temp_data["RI"]
ylen = len(Y)
# X, Y = np.meshgrid(X, Y)



# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)
Z = temp_data["Int"]
# Z = 5
    # sched_r1 = temp_data.loc[temp_data["schedule"] == sched, "R1"]
    
    # Create an empty array of strings with the same shape as the meshgrid, and
    # populate it with two colors in a checkerboard pattern.
    # colortuple = ('y', 'b')
    # colors = np.empty(X.shape, dtype=str)
    # for y in range(ylen):
    #     for x in range(xlen):
    #         colors[y, x] = colortuple[(x + y) % len(colortuple)]
    
    # Plot the surface with face colors taken from the array we made.
surf = ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)
# surf = ax.plot_surface(X, Y, Z, linewidth=0)
# ax.scatter(X, Y, Z)
#summer,viridis,plasma,cividis,RdYlBu,RdYlGn, cmap=cm.cividis
    # Customize the z axis.
ax.set_zlim(-1, 50)
ax.set_xlim(-1, 50)
ax.set_ylim(-1, 120)
ax.set_xlabel('RM')
ax.set_ylabel('RI')
ax.set_zlabel('Intercept')
ax.zaxis.set_major_locator(LinearLocator(6))
    
ax.view_init(30, 30)

plt.show()