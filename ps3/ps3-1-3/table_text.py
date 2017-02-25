# virtual turn table
import sys
import time
import IoRTarm as iort

stat = {}

print("RS and IoT 24-662 Table Control")
# edit IoRTarm.py username to your andrew id
iort.register_user()

while 1:
    stat = iort.check_table_status()
    #print(stat)
    if stat['status'] == 'Running':
        print("table turning")
        ct = time.localtime()
        pt = time.strptime(str(stat['time']), '%Y-%m-%d %H:%M:%S')
        # check the difference of time in second
        if time.mktime(ct)-time.mktime(pt) > 3:
            # when the table stops, it send the new position to server
            newpos = (stat['pos'] + 1) % 8
            print("table stopping")
            iort.table_turn_end(newpos)
    time.sleep(1)

