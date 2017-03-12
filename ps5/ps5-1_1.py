from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import glob
import IoRTcarL as iortl
import math

def moveforward(t = -1):
    print "F"
    stop()
    iortl.forward(1.0*t)
    stop()
    return

def movebackward(t = -1):
    print "B"
    stop()
    iortl.backward(1.0*t)
    stop()
    return

def turnCW(t = -1):
    print "CW"
    #stop()
    iortl.cw(1.0*t)
    #stop()
    return

def turnCCW(t = -1):
    print "CCW"
    #stop()
    iortl.ccw(1.0*t)
    #stop()
    return
    
def stop():
    print "S"
    iortl.stop()
    return

def ConvertToGray(im):
    return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

def MarkRectangeles(contours, img):
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)
    return 
    
def FindContours(imgray):
    contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy 

def FindContoursWithThreshold(img, x, y, z, IsGray=True):
    ret,thresh = cv2.threshold(img,x,y,z)
    if(IsGray==False):
        thresh = ConvertToGray(thresh)
        #ShowGrayImage(thresh)
    contours, hierarchy = FindContours(thresh)
    return contours, hierarchy

def MarkObstacles(image):
    Lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)  
    L = Lab_image[:,:,0]
    B = Lab_image[:,:,2]
    A = Lab_image[:,:,1]
    contoursL, _ = FindContoursWithThreshold(L,225,200,0,True)
    #contoursL = FilterChildsAndSmallBox(c, h)
    contoursB, _ = FindContoursWithThreshold(B,100,150,0,True)
    #contoursB = FilterChildsAndSmallBox(c,h)
    contoursA, _ = FindContoursWithThreshold(A,100,200,0,True)
    MarkRectangeles(contoursL, image)  
    MarkRectangeles(contoursA, image)
    MarkRectangeles(contoursB, image)
    return 

def MinEnclosingCircle(contour, image = None):
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    radius = int(radius)
    if (image is not None):
        cv2.circle(image,center,radius,(0,255,0),1)
    return (x,y,radius)

def getTargetBallColorThresholds():	
    ballLower = (29, 86, 6)
    ballUpper = (80, 200, 125)
    return ballLower, ballUpper

def ConvertToHSV(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)     

def GetMaskForObject(image):
    hsv_image = ConvertToHSV(image)
    ballLower, ballUpper = getTargetBallColorThresholds()
    return cv2.inRange(hsv_image, ballLower, ballUpper)
	
def FindTargetInImage(image):
    print "finding target"
    mask = GetMaskForObject(image)
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
    return circles 
    
def RotateToFindTarget():
    turnCCW(t = 0.25)
    return
    
def TurnRobotTowardsTarget(x,x_size):  
    dist =  1.0*x - (1.0*x_size)/2.0 
    if (dist < 0):
        print "turning CCW"
        turnCCW( 1.0*math.fabs(dist) / (5*x_size))
    else:
        print "turning CW"
        turnCW( 1.0*math.fabs(dist) / (5*x_size))
    return    
    
def MoveRobot(circles, x_size):
    if(len(circles) <= 0):
        RotateToFindTarget()
    else:
        print "target found"
        x = circles[0][0]
        TurnRobotTowardsTarget(x,x_size)
        time.sleep(0.25)
        print "Sleeping"
        moveforward(0.25)
    return

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 10
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(320, 240))

display_window = cv2.namedWindow("Images")

# face detection
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

time.sleep(1)

num = 1
img_list = glob.glob('./*.jpg')
num = len(img_list)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    circles = FindTargetInImage(image)
    print len(circles)
    x_size = np.size(image,1)   
    print x_size
    MoveRobot(circles, x_size)
    # face detection
    #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);
    #faces = face_cascade.detectMultiScale(gray, 1.1, 5);
    #for (x, y, w, h) in faces:
    #    cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Images", image)
    # when you need to store image, please use following command
    #cv2.imwrite("image.jpg", image)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)
    
    if len(circles) > 0:
        if (circles[0][2] > 40):
            print "Reached target"
            camera.close()
            cv2.destroyAllWindows()
            break

    if key == 27 :
        camera.close()
        cv2.destroyAllWindows()
        break
    elif key == ord('c'):
        name = 'capture%02d.jpg' % num
        num = num + 1;
        cv2.imwrite(name, image)

cv2.destroyAllWindows()
