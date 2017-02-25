# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 19:50:44 2017
@author: Ashish Bajaj
Course: 24-662
PS-2
ps2-2-3
"""
#import math as math
import time as time
import win32com.client
    
Eng = win32com.client.Dispatch("CAO.CaoEngine")

def ConnectRoBot():
    ctrl = Eng.Workspaces(0).AddController("RC1", "CaoProv.DENSO.RC8", "",
                                           "Server=127.0.0.1")
    Arm = ctrl.AddRobot("Arm1", "")    
    return ctrl, Arm
    
def Wait(sec):
    time.sleep(sec)
    
def SetUpRobot(Arm):
    #Take arm control
    Arm.Execute("TakeArm", 0)
    
    #Set arm acceleration
    Arm.Accelerate(0, 50.0, -1)
    
    #Set arm speed
    # Actual arm speed (%) = External speed (%) x Internal speed (%)
    Arm.Speed(0, 50)
    Arm.Execute("ExtSpeed", [25])
    
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

def MoveToJ(Arm, Sequence):
    for ele in Sequence:    
        J_Location = "@0 J%d" %ele        
        Arm.Move(1, J_Location , "NEXT")
    return

def TacWeld(Arm):
    print "Tac Welding Start!!"
    MoveToHomePosition(Arm)
    Sequence = [0,1,2,3,4,5,6,7,8,9,10,11,10]
    MoveToJ(Arm, Sequence)
    MoveToHomePosition(Arm)  
    print "Tac Welding Done!!"
    return

def Weld(Arm):
    print "Arc Welding Start!!"
    MoveToHomePosition(Arm)  
    Sequence = [0,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    MoveToJ(Arm, Sequence)
    MoveToHomePosition(Arm)  
    print "Arc Welding Done!!"
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
    
def PerformWelding(Arm):
    #GetArmPosition(Arm)
    #MoveToHomePosition(Arm) 
    TacWeld(Arm)
    Weld(Arm)
    return
    
def main():
    try:
        print "Running the simulation"

        ctrl, Arm = ConnectRoBot()                                
        print "Robot Connected!"

        SetUpRobot(Arm)
        print "SetUp Complete!"
        
        PerformWelding(Arm)        
        CloseConnection(ctrl,Arm)
    except:
        CloseConnection(ctrl,Arm)
    return
    
main()