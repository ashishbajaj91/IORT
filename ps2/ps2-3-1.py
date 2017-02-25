# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 17:43:48 2017
@author: Ashish Bajaj
Course: 24-662
PS-2
ps2-3-1
"""

import numpy as np
import math as math
import win32com.client
    
Eng = win32com.client.Dispatch("CAO.CaoEngine")

InitialPosition = [409.159,19.6189,322.2601,180,44.98757,-177.2548]
HighZ = 320

def MoveToInitialPosition(Arm):
    Arm.Move(1, "@0 J(2.745191,40.80005,90.0,0,3.221371,0)", "NEXT")
    return


def ConnectRoBot():
    ctrl = Eng.Workspaces(0).AddController("RC1", "CaoProv.DENSO.RC8", "",
                                           "Server=127.0.0.1")
    Arm = ctrl.AddRobot("Arm1", "")    
    return ctrl, Arm
  
def SetUpRobot(Arm):
    #Take arm control
    Arm.Execute("TakeArm", 0)
    
    #Set arm acceleration
    Arm.Accelerate(0, 50.0, -1)
    
    #Set arm speed
    # Actual arm speed (%) = External speed (%) x Internal speed (%)
    Arm.Speed(0, 50)
    Arm.Execute("ExtSpeed", [50])
    
    #Set Motor ON
    Arm.Execute("Motor", [1, 0])
    return
    
def CloseConnection(ctrl, Arm):    
    print "\nClosing connection"
    if Arm != None:
        Arm.Execute("GiveArm")
        del Arm

    if ctrl != None:
        del ctrl

    global Eng
    if Eng != None:
        del Eng   

    return

def MoveToHomePosition(Arm):
    Arm.Move(1, "@0 J(0.0,0,0.04,0.05,-0.01,0.07)", "NEXT")
    return
    
def MoveToP(Arm,x,y,z,rx,ry,rz,Method=1):
    Move_Command = "@E P(%f, %f, %f, %f, %f, %f, 1)" %(x,y,z,rx,ry,rz)
    print Move_Command
    Arm.Move(Method, Move_Command, "NEXT")
    return

def GetArmPosition(Arm):
    cur_pos = Arm.AddVariable("@CURRENT_POSITION")
    pos = "%s" %cur_pos
    pos = pos.replace("(","")
    pos = pos.replace(")","")    
    
    pos = pos.split(",")       
    pos = map(float, pos) 

    print "\tThe arm is at P", pos
    return pos     
    
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm

def open_file(file_path, mode):
    "This function return the file pointer"
    return open(file_path, mode)

def read_file(file_pointer):
    "This function reads the contents of the file"
    return file_pointer.readlines()
    
def parse_file(file_data):
    "This function parses the contents of the file"
    content = []
    for line in file_data:
        line = line.split(',')
        if (line[0] == '1' or line[0] == '2'):
            line = map(float,line)
            content.append(line)
    return content  
    
def plot_line(x1,y1,x2,y2,Arm,Z = 290,Method = 1):
    "This function plots a line"   
    
    XFix = 300
    YFix = 0    
    
    X = XFix + y2
    Y = YFix - x2
    MoveToP(Arm, X, Y, Z, 180,37,-177, Method)
    return    
        
def draw_one_pattern(start_vec,pitch_vec,width_vec, Arm):
    for i in range(0,2):
        weave_vec = start_vec + pitch_vec + width_vec
        plot_line(start_vec[0], start_vec[1], weave_vec[0], weave_vec[1], Arm)
        start_vec = weave_vec
        width_vec = -width_vec
    return    
    
def draw_weave_line(start_vec,pitch_vec,width_vec, Arm):
    "This function draws the weave line"
    draw_one_pattern(start_vec,pitch_vec,width_vec, Arm)
    draw_one_pattern(2*pitch_vec + start_vec,pitch_vec,-width_vec, Arm)
    return    

def Draw_End_Weave(start_vec, end_vec, width_vec, pitch_vec, Arm):
    for i in range(0,3):
        weave_vec = start_vec + pitch_vec + width_vec
        plot_line(start_vec[0], start_vec[1], weave_vec[0], weave_vec[1], Arm)
        start_vec = weave_vec
        
        if (i==0):
            width_vec = -width_vec
        if (np.linalg.norm(end_vec - start_vec) < np.linalg.norm(start_vec+pitch_vec)):
            break
    plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1], Arm)
    return

def plot_weave_line(x1,y1,x2,y2,width,pitch, Arm):
    "This function plots a weave pattern for a line"    
    start_vec = np.array([x1,y1,0])
    end_vec = np.array([x2,y2,0])
    vec = end_vec - start_vec
    
    no_of_patterns = int(np.linalg.norm(vec)/pitch)
    
    perpendicular_vec = normalize(np.cross(vec,np.array([0,0,1])))
    
    pitch_vec = 0.25*pitch*normalize(vec)         
    width_vec = 0.5*width*perpendicular_vec    
        
    for count_pattern in range(0,no_of_patterns):
        draw_weave_line(start_vec,pitch_vec,width_vec, Arm)
        start_vec = start_vec + 4.*pitch_vec

    #To check and add the end effect        
    if( 1.*no_of_patterns != np.linalg.norm(vec)/pitch ):
        Draw_End_Weave(start_vec, end_vec, width_vec, pitch_vec, Arm)       
        
    return

def draw_pattern_line(element, Arm):
    "This function draws the line based on the pattern required"

    plot_line(0,0,element[1],element[2],Arm, HighZ)
    if(element[5]!=1):
        plot_weave_line(element[1],element[2],element[3],element[4],element[6],element[7], Arm)
    else:
        plot_line(0,0,element[1],element[2],Arm)        
        plot_line(0,0,element[3],element[4],Arm)
    plot_line(0,0,element[3],element[4],Arm, HighZ)        
    return
        
def get_radial_vector(radius,theta):
    x = radius*math.cos(theta)
    y = radius*math.sin(theta)
    radial_vec = np.array([x,y,0])    
    return radial_vec    
    
def draw_weave_arc(center_vec,radius,delta_theta,theta1,pitch,width, Arm):
    start_vec = center_vec + get_radial_vector(radius,theta1)
    for i in range(0,4):
        width_vec = normalize(get_radial_vector(radius,theta1 + delta_theta/4.))*width
        
        if(i==0 or i==2):            
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.) + width_vec
            width = -width
        else:
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.)
        
        plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1], Arm)
        start_vec = end_vec
        theta1 += delta_theta/4.
    
    return
    
def draw_end_weave_curve(center_vec,radius,delta_theta,theta1,theta2,pitch,width, Arm):
    "This function draws the end weave of curve"    
    start_vec = center_vec + get_radial_vector(radius,theta1)   
    for i in range(0,3):
        width_vec = normalize(get_radial_vector(radius,theta1 + delta_theta/4.))*width
        if(i==0 or i==2):            
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.) + width_vec
            width = -width
        else:
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.)        
                
        plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1], Arm)
        start_vec = end_vec
        theta1 += delta_theta/4.
        if ((theta2-theta1) < (0.75*delta_theta)):
            break
    end_vec = center_vec + get_radial_vector(radius,theta2)        
    plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1], Arm)
    return
    
def plot_weave_arc(x,y,radius,theta1, theta2, width, pitch, Arm):
    "This function plots weave pattern on an arc"    
    center_vec = np.array([x,y,0])

    length_of_arc = math.fabs(radius*(theta2-theta1)*(np.pi/180.))  
    
    no_of_patterns = int(length_of_arc/pitch)
    
    delta_theta = (pitch/radius)
    theta1 = theta1/180.*np.pi
    theta2 = theta2/180.*np.pi
    
    for count_pattern in range(0,no_of_patterns):
        draw_weave_arc(center_vec,radius,delta_theta,theta1,pitch,width*0.5, Arm)
        theta1 += delta_theta

    if(1.*no_of_patterns != length_of_arc/pitch):    
        draw_end_weave_curve(center_vec,radius,delta_theta,theta1,theta2,pitch,width*0.5, Arm)
    return
    
def draw_pattern_arc(element,Arm):
    "This function draws the line based on the pattern required"
    if(element[6]!=1):
        rad_vec = get_radial_vector(element[3],element[4]*np.pi)
        x = element[1] + rad_vec[0]
        y = element[2] + rad_vec[1]
        plot_line(0,0,x,y,Arm, HighZ)

        plot_weave_arc(element[1],element[2],element[3],element[4]*180.,element[5]*180.,-element[7],element[8], Arm)
        
        rad_vec = get_radial_vector(element[3],element[5]*np.pi)
        x = element[1] + rad_vec[0]
        y = element[2] + rad_vec[1]

        plot_line(0,0,x,y,Arm, HighZ)
    return

def plot_file(parsed_data, Arm):
    "This function plots the file from the parsed input"
    for element in parsed_data:
            if(element[0] == 1):
                draw_pattern_line(element, Arm)
            else:
                draw_pattern_arc(element, Arm)
    return
   
def read_and_plot_file(filename, Arm):
    "This function reads and plot the file"
    file_pointer = open_file(filename, 'r')        
    file_data = read_file(file_pointer)
    file_pointer.close()
        
    parsed_data = parse_file(file_data)
    plot_file(parsed_data, Arm)
    return            
    
def main():
    try:
        print "Running the simulation"

        ctrl, Arm = ConnectRoBot()                                
        print "Robot Connected!"

        SetUpRobot(Arm)
        print "SetUp Complete!"

        MoveToHomePosition(Arm)         
        MoveToInitialPosition(Arm)

        "Main function"
        #filename = "2d-shape-1.txt"
        filename = input("Enter FileName in double qoutes:")
        read_and_plot_file(filename, Arm)
        
        MoveToHomePosition(Arm) 
        CloseConnection(ctrl,Arm)
    except:
        print "Error!!"
        CloseConnection(ctrl,Arm)
    return
    
main()