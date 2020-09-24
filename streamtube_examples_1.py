# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 23:07:52 2020

@author: usuario
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D

import streamtubes as st # Import the defined module located in the working directory.



def f(x, y, z):
    
    """
    Arbitrary function defining the radius 
    of the tube at a given point (x, y, z).
    """
    return np.cos(y)**2 + 0.2



# Parameters.

lim = 5 # The plot will have the limits [-lim, lim] on each axis.
num_polygons = 100 # Number of sections that compose each streamtube.
num_sides = 10 # Number of sides of the regular polygon defining the sections.


# Generate the path of the tube. 

x = np.linspace(-lim,lim,num_polygons)
y = np.sin(x)
z = np.cos(x)


# Obtain the radius of the tube at each point in its trajectory.

rs = f(x, y, z)


# Plot the results.

plt.close("all")
fig = plt.figure(figsize=(6,6))
ax  = fig.add_subplot(111, projection="3d", xlim=(-lim,lim), ylim=(-lim,lim), zlim=(-lim,lim))
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

st.plot_streamtube(ax, x, y, z, rs, num_sides=num_sides, color="C0", alpha=0.4, linewidths=0.5, cmap_name="RdYlBu_r", vmin=np.min(rs), vmax=np.max(rs))

plt.tight_layout()
plt.show()
