# control of 24-662 work cell
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Button
import IoRTarm as iort

#plt.ion()

class Index(object):
    def reset(self, event):
        print("Reset")
        val = "Completed"
        iort.set_table_status(val)
        iort.set_camera_status(val)
        iort.set_arm_status(val)

    def turn(self, event):
        print("Turn")
        table = iort.check_table_status()
        camera = iort.check_camera_status()
        arm = iort.check_arm_status()

        ct = time.strptime(str(camera['time']), '%Y-%m-%d %H:%M:%S')
        tt = time.strptime(str(table['time']), '%Y-%m-%d %H:%M:%S')
        at = time.strptime(str(arm['time']), '%Y-%m-%d %H:%M:%S')

        if table['status'] == 'Completed' and camera['status'] == 'Completed' and arm['status'] == 'Completed' and tt <= ct and ct <= at:
            iort.table_turn_start()

            

    
plt_fig = plt.figure('24-662 Virtual WorkCell', figsize=(6,2))
#plt.subplots_adjust(bottom=0.2)

iort.register_user()

# button
callback = Index()
axtable = plt.axes([0.05, 0.1, 0.4, 0.8])
axreset = plt.axes([0.55, 0.1, 0.4, 0.8])
btable = Button(axtable, 'Turn Table')
btable.on_clicked(callback.turn)
breset = Button(axreset, 'Reset Status')
breset.on_clicked(callback.reset)
    
plt.show()
