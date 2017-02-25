# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 14:04:31 2017
@author: Ashish Bajaj
Course: 24-662
PS-1
ps1-3-2
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
    
    fig = plt.figure()
    ax = fig.gca(projection = '3d')  

    x_s1,y_s1= CalculateS1Position(s1)
    x_s2,y_s2= CalculateS2Position(s1,s2)
    z_s3= CalculateS3Position(s3)
    x_s4,y_s4 = CalculateS4Position(s1,s2,s4)

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
    return

def CalculateS3(z):
    s3 = Max_Length_below_vertical - z
    if (s3<0) or (s3 > 200):
        s3 = None
    return s3

def ComputeC(x,y):
    cons = (math.pow(length_arm_2,2.) - (x*x+y*y+math.pow(length_arm_1,2.)))/(2.*length_arm_1)
    return cons
    
def ComputeValue(x,y):
    C = ComputeC(x,y)     
    val = x*x*C*C - ((x*x+y*y)*(C*C- y*y))
    return val

def CalculateS1(x,y):
    C = ComputeC(x,y)    
    value = ComputeValue(x,y) 

    if(value < 0):
        print "Invalid data points"
        return
    sin_s1_1 = (x*C + math.sqrt(value))/(x*x+y*y)    
    sin_s1_2 = (x*C - math.sqrt(value))/(x*x+y*y)

    if (math.fabs(sin_s1_1) <= 1):        
        s1_11 = math.asin(sin_s1_1)
        s1_12 = np.pi - s1_11          
    else: 
        s1_11 = None
        s1_12 = None
        
    if (math.fabs(sin_s1_2) <= 1):   
        s1_21 = math.asin(sin_s1_2)
        s1_22 = np.pi - s1_21
    else: 
        s1_21 = None      
        s1_22 = None
    
    possible_s1 = set([s1_11,s1_12,s1_21,s1_22])
    s1 = []
    for angle in possible_s1:
        if angle != None:
            if( math.fabs(y - (length_arm_1 * math.cos(angle))) <= length_arm_2):
                angle = angle if angle < np.pi else -2*np.pi+angle
                s1.append(angle)                        
    s1 = set(s1)
    return s1

def FilterAngles(un_s1,un_s2):
    s1 = []
    s2 = []    
    for i in range(0,len(un_s1)):
        if (math.fabs(un_s1[i]) <= (155.*(np.pi/180.))) and (math.fabs(un_s2[i]) <= (145.*(np.pi/180.))):
            s1.append(un_s1[i])
            s2.append(un_s2[i])
    return s1,s2

def CalculateS2(p_s1,x,y):
    s2 = []
    s1 = []
    for angle in p_s1:
        angle_cos = (y - (length_arm_1 * math.cos(angle)))/length_arm_2
        full_angle1 = math.acos(angle_cos)
        full_angle2 = -full_angle1
        possible_s2 = set([full_angle1, full_angle2])
        for p_s2 in possible_s2:
            if math.fabs((-length_arm_1*math.sin(angle)-length_arm_2*math.sin(p_s2)) - x) < 10**-6:
                s1.append(angle)                
                s2.append(p_s2-angle)
    Filter_s1, Filter_s2 = FilterAngles(s1,s2)
    return Filter_s1, Filter_s2

def CalculateS4(s1,s2,theta):
    s4 = []
    for i in range(0,len(s1)):
        angle = theta - (s1[i]+s2[i])
        s4.append(angle)        
    return s4
    
def Calculate_S1_S2_S3_S4_Position(x,y,z,theta):
    c_s1 = CalculateS1(x,y)
    s1,s2 = CalculateS2(c_s1,x,y)
    s3 = CalculateS3(z)
    s4 = CalculateS4(s1,s2,theta)
    return s1,s2,s3,s4

def PrintResults(s1, s2, s3, s4):
    if len(s1) <= 0 or s3 == None:
        print "Invalid Configurations"
        return      
    for i in range(0,len(s1)):
        print "\nThe configurations are (s1,s2,s3,s4) = (",s1[i]/np.pi,",",s2[i]/np.pi,",",s3,",",s4[i]/np.pi,")"
        DrawScara(s1[i],s2[i],s3,s4[i])
    plt.show()
    return

def ComputeScaraConfigs(x,y,z,theta):
    "Validates the input,convert to s1,s2,s3,s4 and draws"
    s1, s2, s3, s4 = Calculate_S1_S2_S3_S4_Position(x,y,z,theta)
    PrintResults(s1, s2, s3, s4)
    return
    
def TakeUserInput():
    "Takes and parses the user input"
    position = input("Enter x,y,z,theta (sperated by ,):")   
    #print s_position
    #s_position = s_position.split(",")
    position = map(float,position)
    return position

def main():
    "Main function"
    pos = TakeUserInput()
    if pos[0] == 0 and pos[1] == 0:
        print "Invalid Configurations"
        return
    ComputeScaraConfigs(pos[0],pos[1],pos[2],np.pi*pos[3])    
    return    
       
main()
