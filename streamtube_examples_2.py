# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:01:18 2020

@author: artmenlope

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D

import streamtubes as st # Import the defined module located in the working directory.


def cylinder_flow(Position, t, v=1, r=1):
    
    """
    This is an auxiliar function to be used with Scipy's odeint. 
    Given a point in the space it returns the velocity that an 
    incompressible fluid flowing around a cylinder placed along 
    the y axis would have at that point.

    Input:
        Position :: Array or list containing the x, y, z coordinates.
        t        :: Time (variable for odeint).
        v        :: Float. Magnitude of the velocity.
        r        :: Float. Radius of the cylinder.

    Output: 
        ddt :: Array of velocity components.

    For more information on the theoretical derivation see the following page:
        http://www.vermontveterinarycardiology.com/index.php/for-cardiologists/for-cardiologists?id=127
        ("Velocity and Pressure Distribution for Flow Over a Cylinder")
    """
    
    x = Position[0]
    y = Position[1]
    z = Position[2]
    
    vx =  v * (r**2*(z**2-x**2) + (x**2+z**2)**2) / (x**2+z**2)**2
    vy =  0
    vz = -v * (2*r**2*x*z) / (x**2+z**2)**2
    
    ddt = [vx, vy, vz]

    return ddt



def cylinder_divergence(xi, yi, zi, r, v):
    
    """
    Calculate the divergence of the velocity field returned by 
    the cylinder_flow() function given the path of a streamtube
    providing its path components xi, yi, zi.
    
    The theoretical formula used to calculate the returned 
    variable 'div' has been obtained by hand and is susceptible 
    to errors.

    Input:
        xi, yi, zi :: 1D arrays. Components of the path of the streamtube.
        r :: Float. Radius of the cylinder.
        v :: Float. Modulus of the velocity of the flow.

    Output:
        div :: 1D array. The calculated divergence.
    """
    
    div = -4*v*r**2*xi*zi**2 / (xi**2 + zi**2)**3
    
    return div



def cylinder(x0, y0, z0, r, L, N=20):

    """
    Generate data for a cylinder placed along the y axis.
    
    Input:
        x0, y0, z0 :: Floats. Cylinder's center coordinates.
        r          :: Float. Radius of the cylinder.
        L          :: Float. Length of the cylinder.
        N          :: Integer. The shape of the X, Y, Z arrays will be (N, N).

    Output:
        X, Y, Z :: 3D arrays. Coordinates defining the cylinder's 
                   surface (only the cylinder's side).
    """

    y = np.linspace(-L/2, L/2, N) + y0
    theta = np.linspace(0, 2*np.pi, N) # Using cylindrical coordinates.

    Y, Theta = np.meshgrid(y, theta)
    
    X = r * np.cos(Theta) + x0
    Z = r * np.sin(Theta) + z0

    return X, Y, Z


# Parameters.

lim = 2 # The plot will have the limits [-lim, lim] on each axis.
num_polygons = 100 # Number of sections that compose each streamtube.
num_sides = 8 # Number of sides of the regular polygon defining the sections. 
tubes_perSide = 4 # The streamtubes start at the plane x = -lim, this variable indicates that there will be tubes_perSide**2 streamtubes on the plot in total.


# Generate initial coordinates. 

y0 = np.linspace(-lim, lim, tubes_perSide)
z0 = np.linspace(-lim, lim, tubes_perSide)
Y0, Z0 = np.meshgrid(y0, z0)
# Make the 2D arrays 1-dimensional.
y0s = Y0.reshape(tubes_perSide**2)
z0s = Z0.reshape(tubes_perSide**2)


# Create the time list for odeint to solve the trajectories of the streamtubes.

tf = 4 # Final time (starting time = 0).
t = np.linspace(0, tf, num_polygons) # Times.
nt = len(t) # Number of time steps.


# Calculate the path and divergence of the streamtubes.

tube_path_list = []
divergence_list = []

v = 1 # Modulus of the velocity of the flow.
r = 1 # Radius of the cylinder.

for i in range(tubes_perSide**2):
    
    init_cond_i = [-2, y0s[i], z0s[i]] # Initial conditions of the i'th streamtube.
    path_solution_i = odeint(cylinder_flow, init_cond_i, t, args=(v,r,), atol=1e-6, rtol=1e-4) # Solve for the trajectory.
    xi, yi, zi = path_solution_i.T # Get the path coordinates as 1D arrays.
 
    # Calculate the velocity components.

    vxi =  v * (r**2*(zi**2-xi**2) + (xi**2+zi**2)**2) / (xi**2+zi**2)**2
    vyi =  np.zeros(yi.shape[0])
    vzi = -v * (2*r**2*xi*zi) / (xi**2+zi**2)**2
    
    # Store the results.

    tube_path_list.append([xi, yi, zi, vxi, vyi, vzi])
    divergence_list.append([cylinder_divergence(xi, yi, zi, r, v)])

# Parameters for the plot.

cmap = "coolwarm"
scale_factor = 1/3 # Scale factor for increasing or reducing the thickness of the tubes in general.
vmin = scale_factor*np.min(np.abs(divergence_list)) # vmin and vmax are parameters for using the colormap in the 
vmax = scale_factor*np.max(np.abs(divergence_list)) # st.plot_streamtube function. They indicate the values for the 
                                                    # limits of the colormap. They are passed to Matplotlib.

# Create the axes and the figure. 

plt.close("all")
fig = plt.figure(figsize=(6,6))
ax  = fig.add_subplot(111, projection="3d", 
                      xlim=(-lim,lim), 
                      ylim=(-lim,lim), 
                      zlim=(-lim,lim))
#ax.axis("off")
ax.view_init(elev=5, azim=-100)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


# Plot the cylinder.

Xc, Yc, Zc = cylinder(0, 0, 0, r, 2*lim, 30)
ax.plot_wireframe(Xc, Yc, Zc, alpha=0.4, color="k", linewidth=0.5)


# Plot the streamtubes.

for i in range(tubes_perSide**2):
    
    x, y, z = tube_path_list[i][:3] # Get the streamtube's path coordinates.
    r = scale_factor*np.abs(divergence_list[i][0]) # Array with the radius values of the i'th streamtube.
    
    # Plot the i'th streamtube.
    st.plot_streamtube(ax, x, y, z, r, 
                       num_sides=num_sides, 
                       color="C0", 
                       alpha=1, 
                       linewidths=0.5, 
                       cmap_name=cmap, 
                       vmin=vmin, 
                       vmax=vmax)
    
    
# Show the result.

plt.tight_layout()
plt.show()
