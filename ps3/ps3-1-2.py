# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 20:08:02 2017
@author: Ashish Bajaj
Course: 24-662
PS-3
ps3-1-2
"""
import numpy as np
import itertools as iterools

import win32com.client
    
####################################################################################
### WinCaps Control
####################################################################################
Eng = win32com.client.Dispatch("CAO.CaoEngine")

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
    
def MoveToP(Arm,x,y,z,rx,ry,rz,Method=1):
    Move_Command = "@E P(%f, %f, %f, %f, %f, %f, 1)" %(x,y,z,rx,ry,rz)
    print Move_Command
    Arm.Move(Method, Move_Command, "NEXT")
    return
    
def MoveRobot(Path, HomePosition, Arm):
    XOffset = 800
    YOffset = 0
    
    #Arm.Move(1, "@E P0", "NEXT")
    x = XOffset - HomePosition[0]
    y = -1*HomePosition[1] + YOffset
    rz = HomePosition[2]*180
    MoveToP(Arm, x, y, 100, -180, 0, rz)   

    for ele in Path:
        x = XOffset - ele[0]
        y = -1*ele[1] + YOffset
        rz = ele[2]*180
        MoveToP(Arm, x, y, 100, -180, 0, rz)   
        MoveToP(Arm, x, y, 50, -180, 0, rz)   
        MoveToP(Arm, x, y, 100, -180, 0, rz)   

    x = XOffset - HomePosition[0]
    y = -1*HomePosition[1] + YOffset
    rz = HomePosition[2]*180
    MoveToP(Arm, x, y, 100, -180, 0, rz)   
        
    #Arm.Move(1, "@E P0", "NEXT")
    return

####################################################################################
### WinCaps Control End
####################################################################################

####################################################################################
###Solving Shortest Path
####################################################################################
def GetNorm(v):
    return np.linalg.norm(v)

def open_file(file_path, mode):
    "This function return the file pointer"
    return open(file_path, mode)

def read_file(file_pointer):
    "This function reads the contents of the file"
    return file_pointer.readlines()

def parse_file(file_data):
    "This function parses the contents of the file"
    Red = []
    Green = []
    for line in file_data:
        line = line.replace(" ","")
        line = line.split(',')
        if (line[0] == 'R'):
            line = map(float,line[1:len(line)])
            Red.append(line)
        else:
            if (line[0] == 'G'):
                line = map(float,line[1:len(line)])
                Green.append(line)                
    return Red, Green

def read_and_parse_file(filename):
    file_pointer = open_file(filename, 'r')        
    file_data = read_file(file_pointer)
    file_pointer.close()

    return parse_file(file_data)

def GetVector(Ele):
    return np.array([Ele[0], Ele[1], 0])

def GetPermutations(Size):    
    return list(iterools.permutations(range(Size)))

def GetTotalDistance(Red, Green, Red_P, Green_P, HomePosition):
    
    Distance = GetNorm(GetVector(Red[Red_P[0]]) - GetVector(HomePosition))    
    for i in range(0,len(Green)):
        Distance = Distance + GetNorm(GetVector(Green[Green_P[i]]) - GetVector(Red[Red_P[i]]))
    
    for j in range(1,len(Red)):
        Distance = Distance + GetNorm(GetVector(Red[Red_P[j]]) - GetVector(Green[Green_P[j-1]]))
    
    Distance = Distance + GetNorm(GetVector(HomePosition) - GetVector(Green[Green_P[len(Green) -1]]))        

    return Distance

def FormPath(Red,Green,Red_Order,Green_Order, HomePosition):
    Path = []
    for i in range(0,len(Red)):
        Path.append(Red[Red_Order[i]])
        Path.append(Green[Green_Order[i]])        
    return Path

def FindShortestPath(Red, Green, HomePosition):
    Permutations = GetPermutations(len(Red))

    min_dist = float("inf")   

    for i in range(0,len(Permutations)):
        for j in range(0,len(Permutations)):
            Red_P = Permutations[i]
            Green_P = Permutations[j]
            Dist = GetTotalDistance(Red, Green, Red_P, Green_P, HomePosition)
            
            if (Dist < min_dist):
                min_dist = Dist
                Red_Index = Red_P
                Green_Index = Green_P

    print "The minimum distance is:", min_dist
    Path = FormPath(Red,Green,Red_Index, Green_Index, HomePosition)
    return Path
    
def PrintPathCoordinates(Path, HomePosition):
    print "The Path to be followed is:"    
    print HomePosition
    for ele in Path:
        print ele
    print HomePosition
    return    
####################################################################################
### Shotest Path End
####################################################################################
    
####################################################################################
### Main Functions
####################################################################################
    
def SimulateOnWinCaps(Path, HomePosition):
    try:
        print "Running the simulation"
    
        ctrl, Arm = ConnectRoBot()                                
        print "Robot Connected!"
    
        SetUpRobot(Arm)
        print "SetUp Complete!"
    
        "Main function"
        print "Instructions to Robot are:"
        MoveRobot(Path, HomePosition, Arm)
        CloseConnection(ctrl,Arm)
    except:
        print "Error!!"
        CloseConnection(ctrl,Arm)
    return

def main():
    HomePosition = [600,0,0]

    filename = 'part_positions_1.txt'    
    #filename = 'part_positions_2.txt'
    
    print "Running the simulation for file:", filename

    Red, Green = read_and_parse_file(filename)
    Path = FindShortestPath(Red, Green, HomePosition)
    PrintPathCoordinates(Path, HomePosition)
    SimulateOnWinCaps(Path, HomePosition)
return
    
main()