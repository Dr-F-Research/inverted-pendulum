#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:54:17 2023

@author: anthonyferrar
"""
# This code solves predicts the motion of an inverted pendulum

#import math
import numpy as np
import pygame

#System Properies
#Length of Bar, meters
L = 1
#gravity, m/s^2
g = 9.81

""
# Case 1: 45 degrees
#Initial Condition
theta_0 = 85 *np.pi/180 #radians
omega_0 = 0 #dropped from rest
#Solution Controls
#timestep
deltat = 0.000005 #seconds
#number of steps to take
n = 39


def compute_alpha(g,L,theta):
    alpha = -(3/2)*(g/L)*np.cos(theta)
    return alpha

#Initialize solution variables
alpha_0  = compute_alpha(g,L,theta_0)
OMEGA = omega_0
ALPHA = alpha_0
THETA = theta_0

#prep the animation
pygame.init() 
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("An Inverted Pendulum!")
clock = pygame.time.Clock()
L_scale = 0.8

#Animation Window Setup
origin = (width // 2 , height // 2)     
endx_start1 = np.floor(L*np.cos(THETA)*origin[0]) + origin[0]
endx_start2 = origin[0] - np.floor(L*np.cos(THETA)*origin[0])
endy_start = origin[1] - np.floor(L*np.sin(THETA)*origin[1])

#Run the sim + animate
running = True
frame = 0
frame_skip = 400
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #update angular velocity, omega
    OMEGA_NEW = OMEGA + ALPHA*deltat
    
    #update angular position, theta
    THETA_NEW = THETA + OMEGA*deltat
    
    #update angular acceleration, alpha
    ALPHA_NEW = compute_alpha(g,L,THETA_NEW)
    
    #Draw
    endx = np.floor(L_scale*L*np.cos(THETA_NEW)*origin[0]) + origin[0]
    endy = origin[1] - np.floor(L_scale*L*np.sin(THETA_NEW)*origin[1])
    
    if frame%frame_skip == 0:# or frame%frame_skip == 5:
        if endy < endy_start:
            screen.fill((0,255, 255))
        else:
            screen.fill((255, 255, 255))

        pygame.draw.line(screen, (255,0,0), origin, (endx_start1, endy_start), 2)
        pygame.draw.line(screen, (255,0,0), origin, (endx_start2, endy_start), 2)
        pygame.draw.line(screen, (0,0,0), origin, (endx, endy), 4)
        pygame.display.flip()
        clock.tick(60) #fps
    
    frame = (frame + 1)
    
    OMEGA = OMEGA_NEW
    THETA = THETA_NEW
    ALPHA = ALPHA_NEW

pygame.quit()

