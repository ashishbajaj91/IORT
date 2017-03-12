from __future__ import print_function

import math
import time
import random
import sys, getopt
import httplib, json
import requests as rq
import os
#import IoRTcarL as iortl

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

car_id = 100
username = "24-662"

def reg_car(v1, v2=None):
    global car_id
    if v2 == None:
        v2 = '%s' % username
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "name" : v1,
              "owner" : v2 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_reg_name_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if pdata['ret']:
        car_id = pdata['r_id']
    return pdata;

def get_car_id(v1, v2=None):
    if v2 == None:
        v2 = '%s' % username
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "name" : v1,
              "owner" : v2 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    # conn = httplib.HTTPConnection("localhost")
    # conn.request("POST", "/IoRT/php/pos_w_echo.php", jdata, headers)
    print(jdata)
    conn.request("POST", "/IoRT/php/car_reg_name_r.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if pdata['ret']:
        return pdata['r_id'];
    else:
        return 0;
    
def read_status0(v1=None):
    global car_id
    if v1 == None:
        v1 = car_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : v1 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_stat_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;
    
def read_status(v1, v2=None):
    global username
    if v2 == None:
        v2 = '%s' % username
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "name" : v1,
              "owner" : v2 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_stat_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;

def set_status0(v2, v1=None):
    global car_id
    if v1 == None:
        v1 = car_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : v1,
              "cmd"  : "status",
              "status": v2 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_stat_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;

def park_car(v1=None):
    return set_status0("Parking", v1)
    
def stop_car(v1=None):
    return set_status0("Stop", v1)
    
def write_path(v1, v2, v3=None):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    if v3 == None:
        v3 = '%s' % username
    pdata = { "u_name" : v3,
              "p_name" : v1,
              "path"   : v2 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_path_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    #pdata = json.loads(response.read())

def read_path(v1, v2=None):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    if v2 == None:
        v2 = '%s' % username
    pdata = { "u_name" : v2,
              "p_name" : v1 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_path_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata["path"]

def read_map(var) :
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "m_name" : var }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/car_map_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def write_map(v1, v2, v3=None) :
    if v3 == None:
        v3 = '%s' % username
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "m_name" : v2,
              "u_name" : v3,
              "edge"   : v1 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/car_map_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def read_traffic_map(v1, timestamp=None) :
    if timestamp == None:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "m_name" : v1,
              "t_time" : timestamp }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_traffic_map_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def write_traffic_map(v0, v1, timestamp=None, user=None):
    if timestamp == None:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if user == None:
        user = '%s' % username

    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "traffic" : v1,
              "m_name" : v0,
              "u_name" : user,
              "t_time" : timestamp }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_traffic_map_w.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata

def write_map_img(camera, aux, timestamp, file):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "c_id" : camera,
              "aux" : aux,
              "file" : file,
              "c_time" : timestamp }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_map_img_w1.php", jdata, headers) # write db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if pdata['ret']:
        url = 'http://cerlab29.andrew.cmu.edu/IoRT/php/car_map_img_w2.php'
        fn = os.path.basename(pdata['data']['c_url']);
        #print(fn, file)
        f = {'file': (fn, open(file, 'rb'))}
        r = rq.post(url, files=f)
        return pdata['data']
    else:
        return {}

def read_map_img(camera, ts1=None, ts2=None):
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "c_id" : camera }
    if ts1 != None:
        pdata["ts1"] = ts1
    if ts2 != None:
        pdata["ts2"] = ts2
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn.request("POST", "/IoRT/php/car_map_img_r.php", jdata, headers) # read from db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;


def init(argv):
    iortl.init(argv)

def calibrate():
    iortl.calibrate()

def write_pos(pos_array):
    jdata = json.dumps(pos_array, ensure_ascii = 'False')
    #print(jdata)
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    conn.request("POST", "/IoRT/php/car_pos_w.php", jdata, headers) # write to db
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;

def read_pos(v1, v2, v3=None):
    global car_id
    if v3 == None:
        v3 = car_id
    pdata = { "r_id" : v3 }
    if v1 != None:
        pdata['s_time'] = v1
        if v2 != None:
            pdata['e_time'] = v2
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    #print(jdata)
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    conn.request("POST", "/IoRT/php/car_pos_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    if pdata['ret']:
        return(pdata['pos_array'])
    else:
        return(None)
    
def set_car_pos(pos, dir, v1=None):
    global car_id
    if v1 == None:
        v1 = car_id
    t = time.time()
    s, ms = divmod(int(t*1000.), 1000)
    ts2 = '{}.{:03d}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)), ms)
        
    pos_data = { 'r_id': car_id, 'c_time': ts2, 'pos': pos, 'dir': dir , 'c_url': "", 'c_key': 0}
    pos_arr = []
    pos_arr.append(pos_data)
    return write_pos(pos_array)
    
def get_car_pos(v1=None):
    global car_id
    if v1 == None:
        v1 = car_id
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    pdata = { "r_id" : v1 }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn.request("POST", "/IoRT/php/car_pos_r.php", jdata, headers) # read from DB
    response = conn.getresponse()
    pdata = json.loads(response.read())
    if pdata['ret']:
        return(pdata['pos_array'][0])
    else:
        return(None)

def inc_prog(v1=None):
    if v1 == None:
        v1 = car_id
    pdata = { "r_id" : car_id,
              "cmd" : "inc" }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    conn.request("POST", "/IoRT/php/car_stat_w.php", jdata, headers)
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    #print(pdata)
    return pdata
        
def start_prog(v1, v2=None):
    if v2 == None:
        v2 = '%s' % username
    pdata = { "r_id" : car_id,
              "u_name" : v2,
              "p_name" : v1,
              "cmd" : "start" }
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn = httplib.HTTPConnection("cerlab29.andrew.cmu.edu")
    conn.request("POST", "/IoRT/php/car_stat_w.php", jdata, headers)
    response = conn.getresponse()
    #print(response.read())
    pdata = json.loads(response.read())
    return pdata;
    
