import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Button
import IoRTcarL as iort

#plt.ion()

class Index(object):
  def stop(self, event):
    iort.stop()
    
  def forward(self, event):
    iort.forward(-1.0)

  def backward(self, event):
    iort.backward(-1.0)

  def right(self, event):
    iort.right(-1.0)

  def left(self, event):
    iort.right(-1.0)

  def ccw(self, event):
    iort.ccw(-1.0)

  def cw(self, event):
    iort.cw(-1.0)
    
# main
plt_fig = plt.figure('24-662 Car Control', figsize=(6,3))
#plt.subplots_adjust(bottom=0.2)
# button
callback = Index()
axfwd = plt.axes([0.35, 0.65, 0.3, 0.3])
axbwd = plt.axes([0.35, 0.05, 0.3, 0.3])
axcw  = plt.axes([0.05, 0.35, 0.3, 0.3])
axstp = plt.axes([0.35, 0.35, 0.3, 0.3])
axccw = plt.axes([0.65, 0.35, 0.3, 0.3])

bfwd = Button(axfwd, 'FWD')
bfwd.on_clicked(callback.forward)
bbwd = Button(axbwd, 'BWD')
bbwd.on_clicked(callback.backward)
bcw  = Button(axcw, 'CW')
bcw.on_clicked(callback.cw)
bstp  = Button(axstp, 'STOP')
bstp.on_clicked(callback.stop)
bccw = Button(axccw, 'CCW')
bccw.on_clicked(callback.ccw)

plt.show()
