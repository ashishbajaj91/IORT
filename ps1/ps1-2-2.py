# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 00:11:55 2017
@author: Ashish Bajaj
Course: 24-662
PS-1
ps1-2-2
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np
import math as math

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
    
def plot_line(x1,y1,x2,y2,outputfile,color='k'):
    "This function plots a line"
    x = [x1,x2]
    y = [y1,y2]
    plt.plot(x,y,color)    
    line = [ "1", "%.02f" %x1, "%.02f" %y1, "%.02f" %x2, "%.02f" %y2, "1","0","0"]
    line = ", ".join(line)
    outputfile.write(line)
    outputfile.write("\n")    
    return    
    
def plot_arc(x,y,radius,start_angle,end_angle,ax):
    "This function plots a arc"
    parc = pat.Arc((x,y),2*radius,2*radius,theta1=start_angle,theta2=end_angle)
    ax.add_patch(parc)    
    return

def set_limits(min_x,max_x,min_y,max_y):
    "This function sets the limits for the plot"
    plt.xlim(min_x,max_x)
    plt.ylim(min_y,max_y)
    return
    
def draw_one_pattern(start_vec,pitch_vec,width_vec,outputfile):
    for i in range(0,2):
        weave_vec = start_vec + pitch_vec + width_vec
        plot_line(start_vec[0], start_vec[1], weave_vec[0], weave_vec[1],outputfile)
        start_vec = weave_vec
        width_vec = -width_vec
    return    
    
def draw_weave_line(start_vec,pitch_vec,width_vec,outputfile):
    "This function draws the weave line"
    draw_one_pattern(start_vec,pitch_vec,width_vec,outputfile)
    draw_one_pattern(2*pitch_vec + start_vec,pitch_vec,-width_vec,outputfile)
    return    

def Draw_End_Weave(start_vec, end_vec, width_vec, pitch_vec,outputfile):
    for i in range(0,3):
        weave_vec = start_vec + pitch_vec + width_vec
        plot_line(start_vec[0], start_vec[1], weave_vec[0], weave_vec[1],outputfile)
        start_vec = weave_vec
        
        if (i==0):
            width_vec = -width_vec
        if (np.linalg.norm(end_vec - start_vec) < np.linalg.norm(start_vec+pitch_vec)):
            break
    plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1],outputfile)
    return

def plot_weave_line(x1,y1,x2,y2,width,pitch,outputfile):
    "This function plots a weave pattern for a line"
    #plot_line(x1,y1,x2,y2)
    
    start_vec = np.array([x1,y1,0])
    end_vec = np.array([x2,y2,0])
    vec = end_vec - start_vec
    
    no_of_patterns = int(np.linalg.norm(vec)/pitch)
    
    perpendicular_vec = normalize(np.cross(vec,np.array([0,0,1])))
    
    pitch_vec = 0.25*pitch*normalize(vec)         
    width_vec = 0.5*width*perpendicular_vec    
        
    for count_pattern in range(0,no_of_patterns):
        draw_weave_line(start_vec,pitch_vec,width_vec,outputfile)
        start_vec = start_vec + 4.*pitch_vec

    #To check and add the end effect        
    if( 1.*no_of_patterns != np.linalg.norm(vec)/pitch ):
        Draw_End_Weave(start_vec, end_vec, width_vec, pitch_vec,outputfile)       
        
    return

def draw_pattern_line(element, outputfile):
    "This function draws the line based on the pattern required"
    if(element[5]==1):
        plot_line(element[1],element[2],element[3],element[4],outputfile)
    else:
        plot_weave_line(element[1],element[2],element[3],element[4],element[6],element[7],outputfile)
    return
        
def get_radial_vector(radius,theta):
    x = radius*math.cos(theta)
    y = radius*math.sin(theta)
    radial_vec = np.array([x,y,0])    
    return radial_vec    
    
def draw_weave_arc(center_vec,radius,delta_theta,theta1,pitch,width,outputfile):
    start_vec = center_vec + get_radial_vector(radius,theta1)
    for i in range(0,4):
        width_vec = normalize(get_radial_vector(radius,theta1 + delta_theta/4.))*width
        
        if(i==0 or i==2):            
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.) + width_vec
            width = -width
        else:
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.)
        
        plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1],outputfile)
        start_vec = end_vec
        theta1 += delta_theta/4.
    
    return
    
def draw_end_weave_curve(center_vec,radius,delta_theta,theta1,theta2,pitch,width,outputfile):
    "This function draws the end weave of curve"    
    start_vec = center_vec + get_radial_vector(radius,theta1)   
    for i in range(0,3):
        width_vec = normalize(get_radial_vector(radius,theta1 + delta_theta/4.))*width
        if(i==0 or i==2):            
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.) + width_vec
            width = -width
        else:
            end_vec = center_vec + get_radial_vector(radius,theta1 + delta_theta/4.)        
                
        plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1],outputfile)
        start_vec = end_vec
        theta1 += delta_theta/4.
        if ((theta2-theta1) < (0.75*delta_theta)):
            break
    end_vec = center_vec + get_radial_vector(radius,theta2)        
    plot_line(start_vec[0], start_vec[1], end_vec[0], end_vec[1],outputfile)
    return
    
def plot_weave_arc(x,y,radius,theta1, theta2, width, pitch,outputfile):
    "This function plots weave pattern on an arc"    
    center_vec = np.array([x,y,0])

    length_of_arc = math.fabs(radius*(theta2-theta1)*(np.pi/180.))  
    
    no_of_patterns = int(length_of_arc/pitch)
    
    delta_theta = (pitch/radius)
    theta1 = theta1/180.*np.pi
    theta2 = theta2/180.*np.pi
    
    for count_pattern in range(0,no_of_patterns):
        draw_weave_arc(center_vec,radius,delta_theta,theta1,pitch,width*0.5,outputfile)
        theta1 += delta_theta

    if(1.*no_of_patterns != length_of_arc/pitch):    
        draw_end_weave_curve(center_vec,radius,delta_theta,theta1,theta2,pitch,width*0.5,outputfile)
    return
    
def draw_pattern_arc(element,ax,outputfile):
    "This function draws the line based on the pattern required"
    if(element[6]==1):
        plot_arc(element[1],element[2],element[3],element[4]*180.,element[5]*180., ax)
    else:
        plot_weave_arc(element[1],element[2],element[3],element[4]*180.,element[5]*180.,-element[7],element[8],outputfile)
    return

def plot_file(parsed_data, outputfile):
    "This function plots the file from the parsed input"
    fig = plt.figure()
    ax = fig.gca()
    for element in parsed_data:
            if(element[0] == 1):
                draw_pattern_line(element, outputfile)
            else:
                draw_pattern_arc(element, ax, outputfile)
    set_limits(-150,150,-100,100)    
    return

def get_outputfile_name(inputfilename):
    output_file = inputfilename.split(".")
    output_file[0] = output_file[0] + "-output"
    output_file = '.'.join(output_file)
    return output_file
    
def read_and_plot_file(filename):
    "This function reads and plot the file"
    file_pointer = open_file(filename, 'r')        
    file_data = read_file(file_pointer)
    file_pointer.close()

    output_filename = get_outputfile_name(filename)
    outputfile = open_file(output_filename, 'w')
        
    parsed_data = parse_file(file_data)
    plot_file(parsed_data, outputfile)
    outputfile.close()
    return            
    
def main():
    "Main function"
    InputFiles = ['2d-shape-1.txt','2d-shape-2.txt']
    for filename in InputFiles:
        read_and_plot_file(filename)
    plt.show()
    return

main()