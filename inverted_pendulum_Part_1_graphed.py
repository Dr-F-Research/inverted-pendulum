#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:54:17 2023

@author: anthonyferrar
"""
# This code solves predicts the motion of an inverted pendulum

#import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

#System Properies
#Length of Bar, meters
L = 1
#gravity, m/s^2
g = 9.81

""
# Case 1: 45 degrees
#Initial Condition
theta_0 = 45 *np.pi/180 #radians
omega_0 = 0 #dropped from rest
#Solution Controls
#timestep
deltat = 0.01 #seconds
#number of steps to take
n = 39


"""

#Case 2: 85 degrees
#Initial Condition
theta_0 = 85 *np.pi/180 #radians
omega_0 = 0 #dropped from rest
#Solution Controls
#timestep
deltat = 0.01 #seconds
#number of steps to take
n = 97

"""


def compute_alpha(g,L,theta):
    alpha = -(3/2)*(g/L)*np.cos(theta)
    return alpha

#Initialize solution variables
alpha = [0] * (n+1)
omega = [0] * (n+1)
theta = [0] * (n+1)
t     = [0] * (n+1)

alpha_0  = compute_alpha(g,L,theta_0)
alpha[0] = alpha_0
omega[0] = omega_0
theta[0] = theta_0

#loop through the method
for i in range(n):
    
    #update angular velocity, omega
    omega[i+1] = omega[i] + alpha[i]*deltat
    
    #update angular position, theta
    theta[i+1] = theta[i] + omega[i]*deltat
    
    #update angular acceleration, alpha
    alpha[i+1] = compute_alpha(g,L,theta[i+1])
    
    #update time
    t[i+1] = t[i] + deltat


# Visualize Results
fig1, ax1 = plt.subplots()
line1 = ax1.plot(t,theta)
ax1.grid(True)
plt.show()

# Visualize Results
x1 = 0
y1 = 0

fig, ax = plt.subplots()
ax.grid(True)
ax.axis('equal')
for i in range(n):
    x2 = L*np.cos(theta[i])
    y2 = L*np.sin(theta[i])
    line1 = ax.plot((x1,x2),(y1,y2))
plt.show()