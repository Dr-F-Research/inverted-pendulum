#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:29:08 2023

@author: anthonyferrar
"""
# This code predicts the motion of an inverted pendulum, 
#  with an active PID controller

import numpy as np
import pygame

###############################################################################
#System Properies
#Length of Bar, meters
L = 1 #meters
#Mass of Bar, kg
m = 1 #kg
#gravity, m/s^2
g = 9.81 #m/s^2

###############################################################################
#Initial Condition
theta_0 = -65*np.pi/180 #radians
omega_0 = 0 #dropped from rest
Vx_0 = 0 #m/s

X_0 = 0 #start at origin
FAx_0 = 0 #N, no applied load at the start of the simulation

###############################################################################
#Setpoint + controller properties
goal = 90*np.pi/180 #radians
kP = 7
kI = 1
kD = 1

def PID_control(goal, theta, kP, kI, kD, I, e_old, deltat):
    #error
    e = goal - theta
    
    #PID terms
    P = kP*e
    I = I + kI*e*deltat
    D = kD * (e-e_old)/(deltat)
    
    Fx = P + I + D
    
    return (Fx,e)

###############################################################################
#Solution Controls
#timestep
deltat = 0.000005 #seconds
#frame rate (outer loops per second)
speed = 60
#pendulum scaling
L_scale = 0.8

###############################################################################
#Initialize solution variables

def compute_alpha(g,L,theta,omega,FAx):
    alpha = (3*(omega**2)*np.sin(theta)*np.cos(theta) - (2*g/L)*np.cos(theta)+(6/(m*L))*FAx*np.sin(theta))/(1+3*(np.cos(theta))**2)
    return alpha

alpha_0  = compute_alpha(g,L,theta_0, omega_0,FAx_0)
OMEGA = omega_0
ALPHA = alpha_0
THETA = theta_0
FAX = FAx_0
VX = Vx_0
X = X_0
t = 0


I = 0
e = goal - THETA

###############################################################################
#prep the animation
#Window Setup

width, height = 800, 800

pygame.init() 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("An Inverted Pendulum!")

#reference lines (from where the pendulum was dropped)
origin = (width // 2 , height // 2)     
endx_start1 = np.floor(L*np.cos(THETA)*origin[0]) + origin[0]
endx_start2 = origin[0] - np.floor(L*np.cos(THETA)*origin[0])
endy_start = origin[1] - np.floor(L*np.sin(THETA)*origin[1])



frame = 0
#number of inner loops to run per frame (outer loop)
microtime = int(1//(speed*deltat))
clock = pygame.time.Clock()

def redrawWindow():
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (255,0,0), origin, (endx_start1, endy_start), 2)
    pygame.draw.line(screen, (255,0,0), origin, (endx_start2, endy_start), 2)
    pygame.draw.line(screen, (0,0,0), origin, (endx, endy), 4)

    #Text
    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('V_X = ' + str(VX) + ' m/s', True, (0,0,0), (255,255,255))
    textRect = text.get_rect()
    textRect.center = (400,700)
    screen.blit(text, textRect)

    text2 = font.render('theta = ' + str(THETA*180/np.pi) + ' deg.', True, (0,0,0), (255,255,255))
    textRect2 = text.get_rect()
    textRect2.center = (400,675)
    screen.blit(text2, textRect2)

    text3 = font.render('X = ' + str(X) + ' m', True, (0,0,0), (255,255,255))
    textRect3 = text.get_rect()
    textRect3.center = (400,725)
    screen.blit(text3, textRect3)

    text4 = font.render('t = ' + str(t) + ' sec', True, (0,0,0), (255,255,255))
    textRect4 = text.get_rect()
    textRect4.center = (400,750)
    screen.blit(text4, textRect4)
    pygame.display.update()

###############################################################################
#Run the sim + animate

running = True
while running:
    for i in range(microtime):
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
        
        #Update control horizontal force, FAX
        (FAX_NEW, e) = PID_control(goal, THETA, kP, kI, kD, I, e, deltat)
        
        #update angular acceleration, alpha
        ALPHA_NEW = compute_alpha(g,L,THETA_NEW, OMEGA_NEW,FAX_NEW)
        
        OMEGA = OMEGA_NEW
        THETA = THETA_NEW
        ALPHA = ALPHA_NEW
        VX    = VX_NEW
        X     = X_NEW
        t     = t+deltat
        FAX   = FAX_NEW    
        frame = (frame + 1)
    

    endx = np.floor(L_scale*(L)*np.cos(THETA_NEW)*origin[0]) + origin[0]
    endy = origin[1] - np.floor(L_scale*L*np.sin(THETA_NEW)*origin[1])
    
    clock.tick(speed)
    
    redrawWindow() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()