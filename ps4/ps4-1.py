# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:24:42 2017
@author: Ashish Bajaj
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math as math

def ReadImage(filename):
    img = cv2.imread(filename)
    assert img is not None, "could not read %s"%filename
    return img
    
def ConvertToGray(im):
    return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    
def ConvertBGRToRGB(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

def ShowGrayImage(img):
    plt.imshow(img,cmap='gray')  
    plt.axis('off')
    plt.show()
    return

def drawContours(img, contours):
    cv2.drawContours(img, contours, -1, (0,255,0), 3)
    return img
    
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

def ShowRGBImage(img):
    plt.imshow(ConvertBGRToRGB(img))  
    plt.axis('off')
    plt.show()
    return

def SortContours(contours):
    return sorted(contours, key=cv2.contourArea, reverse=True)

def BlackoutOutsideRegion(img,contours):
    stencil = np.zeros(img.shape).astype(img.dtype)
    color = [255, 255, 255]
    cv2.fillPoly(stencil, contours, color)
    result = cv2.bitwise_and(img, stencil)
    return result

def FindContours(imgray):
    im2, contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy 

def FindContoursWithThreshold(img, x, y, z, IsGray=True):
    ret,thresh = cv2.threshold(img,x,y,z)
    if(IsGray==False):
        thresh = ConvertToGray(thresh)
    contours, hierarchy = FindContours(thresh)
    return contours, hierarchy

def FindAreaOfInterest(img):
    img = AddBlackBorder(img)    
    imgray = ConvertToGray(img)
    contours, hierarchy = FindContoursWithThreshold(imgray,170,255,0)
    contours = SortContours(contours)
    area_of_interest = BlackoutOutsideRegion(img,[contours[0]])
    cropped_image = RemoveBorder(area_of_interest) 
    return cropped_image

def FilterChildsAndSmallBox(contours, hierarchy):
    filtered_contours = []
    for i in range(len(contours)):
        if hierarchy[0,i,3] == -1 and GetAreaOfContour(contours[i]) > 10:
            filtered_contours.append(contours[i])
    return filtered_contours

def GetBoundingBoxes(contours):
    rect_cont = []
    Area = []
    for cnt in contours:
        if(cv2.contourArea(cnt) > 0):
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            rect_cont.append(box)
            Area.append(cv2.contourArea(cnt))
    return rect_cont, Area

def FindCentroid(contour):
    M = cv2.moments(contour)
    cx = 1.0*M['m10']/M['m00']
    cy = 1.0*M['m01']/M['m00']
    return cx, cy

def ComputeOrientations(contours, rect_cont):
    orientations = []    
    for i in range(0,len(contours)):
        cx, cy = FindCentroid(contours[i])
        rx, ry = FindCentroid(rect_cont[i])
        if (rx!=cx):
            ang = math.atan2(ry-cy,rx-cx)
        else:
            if ry>cy:
                ang = np.pi/2
            else:
                ang = -np.pi/2
        orientations.append(ang)
    return orientations
    
def GetCentroidForBoundingBoxes(cont_rect):
    Centroid = []
    for box in cont_rect:
        Centroid.append(FindCentroid(box))
    return Centroid
    
def GetAreaOfContour(contour):
    return cv2.contourArea(contour)    
    
def ClassifyParts(contours, rect_cont):
    Orientations = ComputeOrientations(contours, rect_cont)
    Centroids = GetCentroidForBoundingBoxes(rect_cont)
    Red = []
    Green = []
    for i in range(len(contours)):        
        x = Centroids[i][0]
        y = Centroids[i][1]

        if GetAreaOfContour(contours[i]) > 3000:
            Green.append([x,y,Orientations[i]/np.pi])
        else:
            Red.append([x,y,Orientations[i]/np.pi])
    return Red, Green

def FindParts(img):
    contours, hierarchy = FindContoursWithThreshold(img, 100,100,100, False)
    contours = FilterChildsAndSmallBox(contours, hierarchy)    
    rect_cont, area = GetBoundingBoxes(contours)
    img = drawContours(img, rect_cont)
    Red, Green = ClassifyParts(contours, rect_cont)
    return Red, Green, img 

def GetOutputFileName(Inputfile):
    filename = Inputfile.split(".")[0]
    outputfilename = ''.join([filename, '.txt'])
    return outputfilename

def open_file(file_path, mode):
    return open(file_path, mode)

def WriteToFile(line,outputfile):
    line = ", ".join(line)
    outputfile.write(line)
    outputfile.write("\n")    
    return

def WriteOutputToFile(Red, Green, filename):
    outputfile = open_file(GetOutputFileName(filename), 'w')
    for G in Green:
        line = [ "G", "%.02f" %G[0], "%.02f" %G[1], "%.02f" %G[2]]
        WriteToFile(line,outputfile)
    for R in Red:
        line = [ "R", "%.02f" %R[0], "%.02f" %R[1], "%.02f" %R[2]]
        WriteToFile(line,outputfile)
    outputfile.close()
    return

def DetectParts(img):
    img = FindAreaOfInterest(img)
    Red, Green, img = FindParts(img)
    return Red, Green, img 

def DetectPartsAndWriteToFile(img, filename):
    Red, Green, img = DetectParts(img)
    WriteOutputToFile(Red, Green, filename)
    ShowRGBImage(img)
    return 

def main():
    filename = 'cam_view_mixed.jpg'
    img  = ReadImage(filename)
    DetectPartsAndWriteToFile(img, filename)
    return
    
main()