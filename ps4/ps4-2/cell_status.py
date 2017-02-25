import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import IoRTarm as iort

plt.ion()

def setup(ax):
    ax.cla()
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('none') # bottom
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1)
    #ax.patch.set_alpha(0.0)

def showStatus():
    t = iort.check_table_status()
    t_s = t['status']
    t_t = t['time']
    c = iort.check_camera_status()
    c_s = c['status']
    c_t = c['time']
    a = iort.check_arm_status()
    a_s = a['status']
    a_t = a['time']

    ax = plt.subplot(3, 1, 1)
    setup(ax)
    ax.text(0.1, 0.3, "Table, Position %d\n%s (%s)" % (t['pos'], t_s, t_t), fontsize=24)
    ax = plt.subplot(3, 1, 2)
    setup(ax)
    ax.text(0.1, 0.3, "Camera\n%s (%s)" % (c_s, c_t), fontsize=24)
    ax = plt.subplot(3, 1, 3)
    setup(ax)
    ax.text(0.1, 0.3, "Arm\n%s (%s)" % (a_s, a_t), fontsize=24)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
    plt.show()
    
plt_fig = plt.figure('24-662 Virtual WorkCell Status Monitor', figsize=(8,6))

print("24-662 Status Monitor")
iort.register_user()

while 1:
    #plt.cla()
    showStatus()
    plt.waitforbuttonpress(0.2) # 5fps
