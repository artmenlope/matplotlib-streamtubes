# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:30:44 2020

@author: artmenlope
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R



def polygonYZ(r, x0, y0, z0, n=8):
    
    """
    Generate a polygon in the yz plane. n is the number of sides. 
    n+1 points to generate a closed line.

    Input:
        r          : Float. The radius of the circle where the vertices 
                     of the polygon will be laying.
        x0, y0, z0 : Floats. 3D coordinates of the center of the polygon.
        n          : Number of vertices of the polygon.

    Output:
        Array containing the coordinates of the vertices of the polygon.
    """
    
    angles = np.arange(0,2*np.pi+2*np.pi/n,2*np.pi/n)
    xs = x0 + np.zeros(n+1) 
    ys = y0 + r*np.cos(angles)
    zs = z0 + r*np.sin(angles)
    
    return np.array([xs, ys, zs])



def calc_angles(centers):
    
    """
    Given the centers of the polygon collection calculates the rotation 
    vectors required by scipy.spatial.transform.Rotation.from_rotvec().

    These rotation vectors are calculated in order to rotate the polygons 
    (or streamtube's sections) in a way that the orientation of the plane 
    of each section is aligned with the direction of the streamtube's path.    

    Input: 
        centers : Numpy array of shape (n, 3), where n would be the number 
                  of sections, containing in each row the coordinates of 
                  each streamtube section's center.
    Output:
        rot_vecs : Numpy array of shape (, )
    """

    vec0 = centers[1]-centers[0] #first vec
    vecL = centers[-1]-centers[-2] #Last vec.
    vecsi = centers[2:]-centers[:-2]
    
    vecs = np.vstack((vec0, np.vstack((vecsi, vecL))))
    vecs = (vecs.T/np.linalg.norm(vecs, axis=1)).T
    
    ##################
    xaxis_vec = np.array([1,0,0])
    
    rot_axis_0 = np.cross(xaxis_vec, vecs[0])
    rot_axis_i = np.cross(xaxis_vec, vecs[1:-1])
    rot_axis_L = np.cross(xaxis_vec, vecs[-1])
    
    rot_axis_set = np.vstack((rot_axis_0, np.vstack((rot_axis_i, rot_axis_L))))
    
    rot_angle_0 = np.arccos(np.dot(xaxis_vec, vecs[0].T))
    rot_angle_i = np.arccos(np.dot(xaxis_vec, vecs[1:-1].T))
    rot_angle_L = np.arccos(np.dot(xaxis_vec, vecs[-1].T))
    
    rot_angles = np.hstack((rot_angle_0, rot_angle_i, rot_angle_L))
    rot_vecs = (rot_angles * rot_axis_set.T).T
    
    ##################
    
    return rot_vecs 



def make_sections(x, y, z, r, num_sides=10):
    
    """
    The sections are first oriented along the x axis.
    """
    
    centers = np.stack((x, y, z), axis=1)
    num_centers = centers.shape[0]
    
    sections = np.array([polygonYZ(r[i], *centers[i], n=num_sides) for i in range(num_centers)])
    rot_vecs = calc_angles(centers)
    
    rotated_sections = []
    for i in range(num_centers):
        
        rotation_i = R.from_rotvec(rot_vecs[i])
        rot_section_i = (rotation_i.apply(sections[i].T-centers[i])+centers[i]).T
        rotated_sections.append(rot_section_i)
        
    return np.array(rotated_sections)



def plot_streamtube(ax, x, y, z, r, num_sides=10,
                    color="black", alpha=0.2, linewidths=0.5, 
                    cmap_name=None, vmin=None, vmax=None):
    
    centers = np.stack((x, y, z), axis=1)
    num_centers = centers.shape[0]
    
    sections = make_sections(x, y, z, r, num_sides=num_sides)
    
    if cmap_name is None:
        
        verts = []
        for i in range(num_centers-1):
                
            x1, y1, z1 = sections[i]
            x2, y2, z2 = sections[i+1]
            
            for j in range(num_sides):
                
                verts = [(x1[j  ], y1[j  ], z1[j  ]), (x1[j+1], y1[j+1], z1[j+1]),
                         (x2[j+1], y2[j+1], z2[j+1]), (x2[j  ], y2[j  ], z2[j  ])]
                
                ax.add_collection3d(Poly3DCollection([verts],
                                                      alpha=alpha,
                                                      linewidths=linewidths,
                                                      color=color))
    
    else:
        
        if vmin is None and vmax is None:
            
            cmap = plt.cm.get_cmap(cmap_name)
            
            verts = []
            for i in range(num_centers-1):
                    
                x1, y1, z1 = sections[i]
                x2, y2, z2 = sections[i+1]
                
                for j in range(num_sides):
                    
                    verts = [(x1[j  ], y1[j  ], z1[j  ]), (x1[j+1], y1[j+1], z1[j+1]),
                             (x2[j+1], y2[j+1], z2[j+1]), (x2[j  ], y2[j  ], z2[j  ])]
                    
                    ax.add_collection3d(Poly3DCollection([verts],
                                                          alpha=alpha,
                                                          linewidths=linewidths,
                                                          color=cmap(r[i])))
            
        else:
            
            cmap = plt.cm.get_cmap(cmap_name)
            norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
            
            verts = []
            for i in range(num_centers-1):
                    
                x1, y1, z1 = sections[i]
                x2, y2, z2 = sections[i+1]
                
                color_i = cmap(norm(r[i]))
                
                for j in range(num_sides):
                    
                    verts = [(x1[j  ], y1[j  ], z1[j  ]), (x1[j+1], y1[j+1], z1[j+1]),
                             (x2[j+1], y2[j+1], z2[j+1]), (x2[j  ], y2[j  ], z2[j  ])]
                    
                    ax.add_collection3d(Poly3DCollection([verts],
                                                          alpha=alpha,
                                                          linewidths=linewidths,
                                                          color=color_i))


    
