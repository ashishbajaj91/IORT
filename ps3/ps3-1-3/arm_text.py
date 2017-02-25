import IoRTarm as iort
import time

def move_arm(camera, arm):
    #
    status = "Planning"
    print(status)
    iort.set_arm_status(status)
    
    o_key = camera['o_key']
    obj = iort.read_object_2d(0, o_key)
    print("download %d object data" % (len(obj['obj'])))
    # path planning
    g = []
    r = []
    p = []
    p.append([300,0.0,100, 0])
    for o in obj['obj']:
        if o['o_type'] == 'R':
            r.append(o)
        elif o['o_type'] == 'G':
            g.append(o)
    ang = 0.0
    print("move to 300., 0.")
    for i in range(len(g)):
        print("move to %g %g ang %g" % (r[i]['pos_x'], r[i]['pos_y'], ang))
        ang += g[i]['rot'] - r[i]['rot'];
        print("move to %g %g ang %g" % (g[i]['pos_x'], g[i]['pos_y'], ang))
    print("move to 300., 0.")
              
    time.sleep(2)

    # move
    status = "Running"
    
    print(status)
    iort.set_arm_status(status)
    #
    time.sleep(2)

    # clear status
    status = "Completed"
    print(status)
    iort.set_arm_status(status)
    
print("RS and IoT 24-662 Robot Control")
iort.register_user()

while 1:
    table = iort.check_table_status();
    camera = iort.check_camera_status();
    arm = iort.check_arm_status();

    tt = time.strptime(str(table['time']), '%Y-%m-%d %H:%M:%S')
    ct = time.strptime(str(camera['time']), '%Y-%m-%d %H:%M:%S')
    at = time.strptime(str(arm['time']), '%Y-%m-%d %H:%M:%S')

    #print(arm['status'])
    # PS3 ... you need to check every condition 
    if arm['status'] == 'Completed' and camera['status'] == 'Completed' and table['status'] == 'Completed':
        move_arm(camera, arm)
    time.sleep(2)

