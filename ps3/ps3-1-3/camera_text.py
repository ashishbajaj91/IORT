# virtual camera control
import cv2
from skimage import io
import numpy as np
import sys
import time
import os
import IoRTarm as iort

def process_camera(c_id, t_pos):
    val = 'Capturing'
    print(val)
    table = iort.set_camera_status(val)
    # it is not necessary to sleep, however, this sleep shows the Capturing
    # status in cell_status.py
    time.sleep(1)

    #print("cid %d, t_pos %d" % (c_id, t_pos))
    
    # Real image caputre (it is comment out since we provide image in PS3/4)
    # OpenCV video capture (comment out when you capture it)

    
    #cap = cv2.VideoCapture(0)
    #cap.set(3, 1280) # WIDTH : MAX 1920, 3 ... CV_CAP_PROF_WIDTH
    #cap.set(4, 720)  # HEIGHT: MAX 1080, 4 ... CV_CAP_PROF_HEIGHT
    #cap.set(5, 30)   # FPS   : MAX 60,   5 ... CV_CAP_PROF_FPS
    #ret, frame = cap.read()
    #assert ret
    #cv2.imwrite("image.jpg", frame)
    
    # Upload image (PS3: any image, PS4: provided image)
    t = time.time()
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    camera = iort.write_camera_2d(c_id, t_pos, ts, 'image.jpg') # change file name in PS4
    c_key = camera['c_key']
    
    #print(c_key)

    val = 'Recognizing'
    print(val)
    iort.set_camera_status(val, i_key = c_key)
    time.sleep(1) # same reason to sleep
    
    # download image file from server
    camera_image = iort.read_camera_2d(0, 0, c_key)
    #print(camera_image)
    print "downloading %s" % (camera_image[0]['c_url'])
    image = io.imread(camera_image[0]['c_url'])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # PS3 (no recognition), this program uploads the given file information
    if (t_pos % 2) == 0:
        obj = [{u'pos_x': 275, u'pos_y': 60, u'o_type': u'G', u'c_key': 1, u'u_name': 0, u'aux': 1, u'rot': -0.45}, {u'pos_x': 185, u'pos_y': 20, u'o_type': u'G', u'c_key': 1, u'u_name': 0, u'aux': 1, u'rot': -0.75}, {u'pos_x': 315, u'pos_y': 195, u'o_type': u'R', u'c_key': 1, u'u_name': 0, u'aux': 1, u'rot': -0.25}, {u'pos_x': 165, u'pos_y': 115, u'o_type': u'R', u'c_key': 1, u'u_name': 0, u'aux': 1, u'rot': 0.8}]
    else:
        obj = [{u'pos_x': 200, u'pos_y': 25, u'o_type': u'G', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0}, {u'pos_x': 200, u'pos_y': 100, u'o_type': u'G', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0}, {u'pos_x': 325, u'pos_y': 25, u'o_type': u'G', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0}, {u'pos_x': 325, u'pos_y': 100, u'o_type': u'G', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0}, {u'pos_x': 100, u'pos_y': 50, u'o_type': u'R', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0.25}, {u'pos_x': 250, u'pos_y': 200, u'o_type': u'R', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0.5}, {u'pos_x': 300, u'pos_y': 150, u'o_type': u'R', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0}, {u'pos_x': 300, u'pos_y': 225, u'o_type': u'R', u'c_key': 2, u'u_name': 0, u'aux': 2, u'rot': 0.5}]

    # PS4: OpenCV recognition part here

    # finalize
    print("upload %d object information" % (len(obj)))
    object = iort.write_object_2d(c_key, obj)
    val = 'Completed'
    print(val)
    iort.set_camera_status(val, o_key=object['o_key'])

stat = {}

print("RS and IoT 24-662 Camera Control")
#print os.getcwd()
iort.register_user()

while 1:
    table = iort.check_table_status()
    camera = iort.check_camera_status()
    arm = iort.check_arm_status()

    # in order to compare the time, you need to bring string data to time structure.
    ct = time.strptime(str(camera['time']), '%Y-%m-%d %H:%M:%S')
    tt = time.strptime(str(table['time']), '%Y-%m-%d %H:%M:%S')
    at = time.strptime(str(arm['time']), '%Y-%m-%d %H:%M:%S')

    if table['status'] == 'Completed' and camera['status'] == 'Completed' and arm['status'] == 'Completed' and ct < tt and ct <= at:
        process_camera(camera['c_id'], table['pos'])
    time.sleep(1)

