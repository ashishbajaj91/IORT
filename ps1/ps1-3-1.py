# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 22:14:47 2017
@author: Ashish Bajaj
Course: 24-662
PS-1
ps1-3-1
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pat
import mpl_toolkits.mplot3d.art3d as art3d
import math as math
import numpy as np

z_height = 377
length_arm_1 = 125.0
length_arm_2 = 225.0
length_arm_3 = 30
circle1_radius = 65
circle2_radius = 40
circle3_radius = 30
Total_Len_of_vertical_Arm = 451.0
Max_Length_below_vertical = 246.0 

def DrawLine(x1,y1,z1,x2,y2,z2, ax, color ='k'):
    x = [x1, x2]
    y = [y1, y2]
    z = [z1, z2]    
    ax.plot(x,y,z,color)    
    return
    
def DrawRectangle(x,y,z,width,height,ax,edgecolor,facecolor,alpha=1):
    rect = pat.Rectangle((x,y),width,height,edgecolor=edgecolor,facecolor=facecolor,alpha=alpha)
    ax.add_patch(rect)
    art3d.pathpatch_2d_to_3d(rect, z = z, zdir = 'z')
    return
 
def DrawCircle(x,y,z,radius,edgecolor,facecolor,ax):
    circ = pat.Circle((x,y), radius, edgecolor=edgecolor, facecolor=facecolor, alpha = 0.7)
    ax.add_patch(circ)
    art3d.pathpatch_2d_to_3d(circ, z = z, zdir = 'z')
    return

def DrawBase(ax):
    DrawRectangle(-75,75,0,150,-192,ax,'red','#d3d3d3')
    return

def DrawCircle1(ax):
    DrawCircle(0,0,z_height,circle1_radius,'red','#d3d3d3',ax)
    return
    
def DrawAxis1(ax):
    DrawLine(0,0,0,0,0,z_height, ax, color ='b')
    return

def DrawCircle2(x,y,ax):
    DrawCircle(x,y,z_height,circle2_radius,'red','#d3d3d3',ax)    
    return
    
def DrawJoint2(x,y,ax):
    DrawLine(0,0,z_height,x,y,z_height, ax, color ='b')
    return
    
def DrawCircle3(x,y,ax):
    DrawCircle(x,y,z_height,circle3_radius,'red','#d3d3d3',ax)    
    return
    
def DrawJoint3(x_s1,y_s1,x_s2,y_s2,ax):
    DrawLine(x_s1,y_s1,z_height,x_s2,y_s2,z_height, ax, color ='b')    
    return

def DrawJoint4(z_s3,x_s2,y_s2,ax):
    DrawLine(x_s2,y_s2,z_s3,x_s2,y_s2,z_s3+Total_Len_of_vertical_Arm, ax, color ='b')    
    return

def DrawJoint5(x_s4,y_s4,x_s2,y_s2,z_s3,ax):
    DrawLine(x_s4,y_s4,z_s3,x_s2,y_s2,z_s3, ax, color ='b')    
    return

def Validate_Inputs(s1,s2,s3):
    error = 0    
    if (math.fabs(s1) > (155.*(np.pi/180.))):
        print("The first joint is out of the range. Please input a valid number.\n")
        error = 1

    if (math.fabs(s2) > (145.*(np.pi/180.))):
        print("The second joint is out of the range. Please input a valid number.\n")
        error = 1

    if ( (s3<0) or (s3 > 200)):
        print("The third joint is out of the range. Please input a valid number.\n")
        error = 1
        
    return error

def CalculateS1Position(s1):
    y = length_arm_1*math.cos(s1)
    x = -length_arm_1*math.sin(s1)    
    return x,y

def CalculateS2Position(s1,s2):
    y_s2 = length_arm_2*math.cos(s1+s2)
    x_s2 = -length_arm_2*math.sin(s1+s2)    
    x_s1, y_s1 = CalculateS1Position(s1)
    x = x_s1 + x_s2
    y = y_s1 + y_s2
        
    return x,y

def CalculateS3Position(s3):
    z = Max_Length_below_vertical - s3
    return z
    
def CalculateS4Position(s1,s2,s4):
    y_s4 = length_arm_3*math.cos(s1+s2+s4)
    x_s4 = -length_arm_3*math.sin(s1+s2+s4)    
    x_s2, y_s2 = CalculateS2Position(s1,s2)    
    x = x_s4 + x_s2
    y = y_s4 + y_s2
            
    return x,y

def PrintResult(x,y,z,theta):
    print "\nThe hand position and orientation (x,y,z,theta) = (",x,",",y,",",z,",",theta, ")"
    return

def Set_Limits(ax):
    "Set the limits on graph display"
    ax.set_xlim3d(-500,500)
    ax.set_ylim3d(-500,500)
    ax.set_zlim3d(0,700)    
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    ax.set_zlabel("z-axis") 
    return

def DrawScara(s1,s2,s3,s4):

    if(Validate_Inputs(s1,s2,s3) > 0):
        return
        
    fig = plt.figure()
    ax = fig.gca(projection = '3d')  

    x_s1,y_s1= CalculateS1Position(s1)
    x_s2,y_s2= CalculateS2Position(s1,s2)
    z_s3= CalculateS3Position(s3)
    x_s4,y_s4 = CalculateS4Position(s1,s2,s4)
    
    theta = s1+s2+s4
    PrintResult(x_s2,y_s2,z_s3,theta/np.pi)
        
    #Dwaw the base and first axies
    DrawBase(ax)
    DrawCircle1(ax)
    DrawAxis1(ax)
    #Draw the second circle
    DrawCircle2(x_s1,y_s1,ax)
    DrawJoint2(x_s1,y_s1,ax)    
    #Draw the third circle
    DrawCircle3(x_s2,y_s2,ax)
    DrawJoint3(x_s1,y_s1,x_s2,y_s2,ax)
    #Draw the s3 axis    
    DrawJoint4(z_s3,x_s2,y_s2,ax)    
    #Draw the s4 line
    DrawJoint5(x_s4,y_s4,x_s2,y_s2,z_s3,ax)    
    
    Set_Limits(ax)
    plt.show()
    return

def TakeUserInput():
    "Takes and parses the user input"
    s_position = input("Enter s1,s2,s3,s4 (sperated by ,):")   
    #print s_position
    #s_position = s_position.split(",")
    s_position = map(float,s_position)
    return s_position

def main():
    "Main Function"
    s_pos = TakeUserInput()
    DrawScara(np.pi*s_pos[0],np.pi*s_pos[1],s_pos[2],np.pi*s_pos[3])
    return

main()

