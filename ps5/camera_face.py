from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(320, 240))

display_window = cv2.namedWindow("Images")

# face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

time.sleep(1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    # face detection
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY);
    faces = face_cascade.detectMultiScale(gray, 1.1, 5);
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Images", image)
    key = cv2.waitKey(1)

    rawCapture.truncate(0)

    if key == 27:
        camera.close()
        cv2.destroyAllWindows()
        break
