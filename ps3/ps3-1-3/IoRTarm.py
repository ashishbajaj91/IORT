from __future__ import print_function

import math
import time
import random
import sys, getopt
import httplib, json
import requests as rq
import os

username = "ashishb4098"
robot_id = 1
table_id = 1
camera_id = 1

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

def check_arm_status():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_stat_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def set_arm_status(status):
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print(p_name)
    pdata = { "r_id" : robot_id,
              "cmd"  : "status",
              "status" : status }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    return(pdata['ret']);

def check_status():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_stat_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def arm_check_status():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_stat_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def arm_set_status(status):
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id,
              "cmd" : "status",
              "status" : status }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def write_prog(p_name, user, o_key, prog):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print(p_name)
    pdata = { "p_name" : p_name,
              "u_name" : user,
              "o_key"  : o_key,
              "prog"   : prog }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_prog_w.php", jdata, headers) # db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return(pdata)
    
    
def read_prog(p_name, user):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print(p_name, user)
    pdata = { "p_name" : p_name,
              "u_name" : user }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_prog_r.php", jdata, headers) # db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if (pdata['ret']):
        return(pdata['data'])
    else:
        return null

def stop_arm():
    print("stopping arm")
    # once success
    reset_status()

def stop_prog():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print(p_name)
    pdata = { "r_id" : robot_id,
              "cmd"  : "stop"
    }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    return(pdata['ret']);

def start_prog(p_name, user):
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print(p_name)
    pdata = { "r_id" : robot_id,
              "cmd"  : "start",
              "p_name" : p_name,
              "u_name" : user
    }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return(pdata['ret']);
    
def run_prog(seq, prog):
    cmd = prog[seq]
    print("move arm by following command %s %f %f %f" % (cmd['cmd'], cmd['pos_x'], cmd['pos_y'], cmd['pos_z']))
    return True

def inc_prog_seq():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id,
              "cmd"  : "inc" }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    return pdata['ret']

def reset_status():
    global robot_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : robot_id,
              "cmd"  : "reset" }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    pdata = json.loads(response.read())
    return pdata['ret']

def register_user(name=None):
    global robot_id, table_id, camera_id, username

    if name != None:
        username = '%s' % name
        
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "name" : username }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_reg_name.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    robot_id = int(pdata['r_id'])
    table_id = int(pdata['t_id'])
    camera_id = int(pdata['c_id'])
    username = '%s' % name
    #print(robot_id)
    return pdata['ret']
    
def write_camera_2d(camera, aux, timestamp, file):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "c_id" : camera,
              "aux" : aux,
              "file" : file,
              "c_time" : timestamp }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_camera_2d_w1.php", jdata, headers) # write db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if pdata['ret']:
        url = 'http://cerlab29.andrew.cmu.edu/IoRT/php/arm_camera_2d_w2.php'
        fn = os.path.basename(pdata['data']['c_url']);
        #print(fn, file)
        f = {'file': (fn, open(file, 'rb'))}
        r = rq.post(url, files=f)
        return pdata['data']
    else:
        return {}


def read_camera_2d(camera, timestamp, c_key=None):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    if c_key is None:
        pdata = { "c_id" : camera,
	          "c_time" : timestamp }
    else:
        pdata = { "c_key" : c_key }
        
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/arm_camera_2d_r.php", jdata, headers) # read from db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata['data']

def read_object_2d(camera_key, obj_key=None):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    if obj_key is None:
        pdata = { "c_key" : camera_key,
	          "u_name" : username }
    else:
        pdata = { "o_key" : obj_key }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_obj_2d_r.php", jdata, headers) # read from db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata['data']

def write_object_2d(camera_key, obj):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    #print("c_key: %d" % camera_key)
    #print("user: %s" % user)
    #print(obj)
    pdata = { "c_key"  : camera_key,
              "u_name" : username,
              "obj"    : obj }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/arm_obj_2d_w.php", jdata, headers) # write db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata

def table_turn_start():
    global table_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = {
        "t_id" : table_id,
        "cmd" : "turn"
    }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/table_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata['ret']


def table_turn_end(newpos):
    global table_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = {
        "t_id" : table_id,
        "cmd" : "done",
        "pos" : newpos
    }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/table_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata['ret']


def check_table_status():
    global table_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "t_id" : table_id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/table_stat_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def set_table_status(status):
    global table_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = {
        "t_id" : table_id,
        "cmd" : "status",
        "status" : status
    }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/table_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def check_camera_status():
    global camera_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "c_id" : camera_id }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/camera_stat_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def set_camera_status(status, i_key=None, o_key=None):
    global camera_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = {
        "c_id" : camera_id,
        "cmd" : "status",
        "status" : status,
    }
    if i_key != None:
        pdata['i_key'] = i_key
    if o_key != None:
        pdata['o_key'] = o_key
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/camera_stat_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata
