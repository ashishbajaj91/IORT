# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:09:17 2017
@author: Ashish Bajaj
"""

import IoRTcarL as iortl
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import math
import glob

def moveforward(t = -1):
    print "F"
    iortl.forward(1.0*t)
    return

def movebackward(t = -1):
    print "B"
    iortl.backward(1.0*t)
    return

def turnCW(t = -1):
    print "CW"
    iortl.cw(1.0*t)
    return

def turnCCW(t = -1):
    print "CCW"
    iortl.ccw(1.0*t)
    return
    
def stop():
    print "S"
    iortl.stop()
    return

def SetUpCamera():
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 30
    camera.hflip = True
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(320, 240))
    return camera, rawCapture    

def OpenDisplayWindow(name):
    cv2.namedWindow(name)
    return
    
def DestroyWindow(name = None):
    if (name == None):
        cv2.destroyAllWindows()
    else:
        cv2.destroyWindow(name)
    return

def ShowImage(window_name, image):
    cv2.imshow(window_name, image)
    return

def ConvertBGRToRGB(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
def ShowBGRImage(image):
    plt.imshow(ConvertBGRToRGB(image))  
    return
    
def ConvertToGray(im):
    return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    
def ShowGrayImage(img):
    plt.imshow(img,cmap='gray')  
    plt.show()
    return

def BlackoutOutsideRegion(img,contours):
    stencil = np.zeros(img.shape).astype(img.dtype)
    color = [255, 255, 255]
    cv2.fillPoly(stencil, contours, color)
    result = cv2.bitwise_and(img, stencil)
    return result

def MinEnclosingCircle(contour, image = None):
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    radius = int(radius)
    if (image is not None):
        cv2.circle(image,center,radius,(0,255,0),1)
    return (x,y,radius)

def FindTargetInImage(image):
    print "finding target"
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)     
    ballLower = (29, 86, 6)
    ballUpper = (80, 200, 125)
    mask = cv2.inRange(hsv_image, ballLower, ballUpper)

    contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    circles = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 15) & (area > 30) ):
            circle = MinEnclosingCircle(contour, image)       
            circles.append(circle)
            
    if len(circles) > 1:
        print "Found more than one target"
        
    #ShowBGRImage(image)
    return circles 

def RotateToFindTarget():
    turnCW(t = 0.05)
    return
    
def TurnRobotTowardsTarget(x,x_size):  
    dist =  1.0*x - (1.0*x_size)/2.0 
    if (dist < 0):
        print "turning CCW"
        turnCCW( 1.0*math.fabs(dist) / (10*x_size))
    else:
        print "turning CW"
        turnCW( 1.0*math.fabs(dist) / (10*x_size))
    return    
    
def MoveRobot(circles, x_size):
    if(len(circles) <= 0):
        RotateToFindTarget()
    else:
        print "target found"
        #print circles
        x = circles[0][0]
        #print x, x_size
        TurnRobotTowardsTarget(x,x_size)
        moveforward(0.10)
    return
    

def drawContours(img, contours):
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    return img

def FindContours(imgray):
    im2, contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy 

def GetAreaOfContour(contour):
    return cv2.contourArea(contour)    

def FilterChildsAndSmallBox(contours, hierarchy):
    filtered_contours = []
    for i in range(len(contours)):
        if hierarchy[0,i,3] == -1 and GetAreaOfContour(contours[i]) > 0:
            filtered_contours.append(contours[i])
    return filtered_contours

def FindContoursWithThreshold(img, x, y, z, IsGray=True):
    ret,thresh = cv2.threshold(img,x,y,z)
    if(IsGray==False):
        thresh = ConvertToGray(thresh)
        #ShowGrayImage(thresh)
    contours, hierarchy = FindContours(thresh)
    return contours, hierarchy


def AddBlackBorder(img):
    color = [0, 0, 0]
    top, bottom, left, right = [50]*4
    img_with_border = cv2.copyMakeBorder(img, top, bottom, left, right, 0,value=color)
    return img_with_border 

def RemoveBorder(img):
    wid = img.shape[1]
    hei = img.shape[0]
    crop_img = img[50:hei-50,50:wid-50]    
    return crop_img 

def FindContoursForMasks(masks):
    Obstacles = []    
    for mask in masks:
        contours = FilterChildsAndSmallBox(FindContours(mask))     
        Obstacles = Obstacles + contours 
    return

def MarkRectangeles(contours, img):
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)
    return     
   
def MarkObstacles(image):
    image = AddBlackBorder(image)
    Lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)  
    L = Lab_image[:,:,0]
    B = Lab_image[:,:,2]
    A = Lab_image[:,:,1]
    contoursL, _ = FindContoursWithThreshold(L,225,200,0,True)
    #contoursL = FilterChildsAndSmallBox(c, h)
    contoursB, _ = FindContoursWithThreshold(B,100,150,0,True)
    #contoursB = FilterChildsAndSmallBox(c,h)
    contoursA, _ = FindContoursWithThreshold(A,100,200,0,True)
    #contoursA = FilterChildsAndSmallBox(c, h)
    
    #MarkRectangeles(contoursL, image)  
    #MarkRectangeles(contoursA, image)
    #MarkRectangeles(contoursB, image)
    #drawContours(image, contoursL)
    #drawContours(image, contoursB)
    #drawContours(image, contoursA)
    
    #ShowBGRImage(RemoveBorder(image))
#    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)     
#
#    blueLower = (90, 50, 50)
#    blueUpper = (130, 255, 255)
#
#    greenLower = (29, 86, 6)
#    greenUpper = (64, 255, 255)
#
#    orangeLower = (0, 150, 100)
#    orangeUpper = (40, 250, 250)
#    
#    masks = []
#    masks.append(cv2.inRange(hsv_image, blueLower, blueUpper))
#    masks.append(cv2.inRange(hsv_image, greenLower, greenUpper))
#    masks.append(cv2.inRange(hsv_image, orangeLower, orangeUpper))
#    
#    FindContoursForMasks(masks)    
    
#    blue = cv2.bitwise_and(image,image,mask = bluemask)    
#    green = cv2.bitwise_and(image,image,mask = greenmask)    
#    orange = cv2.bitwise_and(image,image,mask = orangemask)    
    return

def movetoTarget(camera, rawCapture):
    Raw_Feed_Window = "Raw_Feed"
    #OpenDisplayWindow(Raw_Feed_Window)
    counter = 1
    while(1):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            print counter
            counter +=1
            #ShowImage(Raw_Feed_Window, image)
            rawCapture.truncate(0)
            MoveRobot(FindTargetInImage(image), np.size(image,1))
    print "it exited from loop"
    return

def main():
    camera, rawCapture = SetUpCamera()    
    movetoTarget(camera, rawCapture)
    return

try:
    stop()
    main()
    stop()
except:
    print "error"
    stop()
