#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:29:08 2023

@author: anthonyferrar
"""
# This code solves predicts the motion of an inverted pendulum, with a horizontal driving force at the pin

#import math
import numpy as np
import pygame

#System Properies
#Length of Bar, meters
L = 1
#Mass of Bar, kg
m = 1
#gravity, m/s^2
g = 9.81

""
# Case 1: 45 degrees
#Initial Condition
FAx_0 = .25 #N
Vx_0 = 0 #m/s
theta_0 = 85 *np.pi/180 #radians
omega_0 = 0 #dropped from rest
X_0 = 0 #start at origin
#Solution Controls
#timestep
deltat = 0.000005 #seconds


def compute_alpha(g,L,theta,omega,FAx):
    alpha = (3*(omega**2)*np.sin(theta)*np.cos(theta) - (2*g/L)*np.cos(theta)+(6/(m*L))*FAx*np.sin(theta))/(1+3*(np.cos(theta))**2)
    return alpha

#Initialize solution variables
alpha_0  = compute_alpha(g,L,theta_0, omega_0,FAx_0)
OMEGA = omega_0
ALPHA = alpha_0
THETA = theta_0

FAX = FAx_0
VX = Vx_0
X = X_0


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
    
    #Update horizontal acceleration, AX
    AX = FAX/m
    
    #Update horizontal velocity, Vx
    VX_NEW = VX + AX*deltat
    
    #Update horizontal position, X
    X_NEW = X + VX*deltat
    
    #Update horizontal force, FAX
    FAX_NEW = FAX #add function here
    
    #update angular acceleration, alpha
    ALPHA_NEW = compute_alpha(g,L,THETA_NEW, OMEGA_NEW,FAX_NEW)
    
    #Draw - fix this!!!!!
    endx = np.floor(L_scale*(L)*np.cos(THETA_NEW)*origin[0]) + origin[0]
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
    VX    = VX_NEW
    X     = X_NEW
    FAX   = FAX_NEW
    
    
    

pygame.quit()

