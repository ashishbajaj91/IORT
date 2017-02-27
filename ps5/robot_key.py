import time
import sys, tty, termios

import IoRTcarL as iortl

def getch():
  import sys, tty, termios
  old_settings = termios.tcgetattr(0)
  new_settings = old_settings[:]
  new_settings[3] &= ~termios.ICANON
  try:
    termios.tcsetattr(0, termios.TCSANOW, new_settings)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(0, termios.TCSANOW, old_settings)
  return ch

try:
  while 1:
    c = getch()
    if c == 'w' or c == 'W':
      print("FWD")
      iortl.forward(-1.0)
    elif c == 'x' or c == 'X':
      print("BWD")
      iortl.backward(-1.0)
    elif c == 'd' or c == 'D':
      print("CW")
      iortl.cw(-1.0)
    elif c == 'a' or c == 'A':
      print("CCW")
      iortl.ccw(-1.0)
    elif c == 's' or c == 'S':
      print("STOP")
      iortl.stop()
      
except:
  iortl.stop()
