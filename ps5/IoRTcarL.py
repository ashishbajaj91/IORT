import RPi.GPIO as gpio
import time

pr1 = 30  # forward/backward pwm ratio
pr2r = 50 # fast side pwm ratio for right
pr2l = 40 # fast side pwm ratio for left
pr3r = 20 # slow side pwm ratio  for right
pr3l = 20 # slow side pwm ratio for left
pr4 = 60  # ccw/cw pwm ratio

pwm11 = None
pwm12 = None
pwm13 = None
pwm15 = None

def init():
  global pwm11, pwm12, pwm13, pwm15
  gpio.setmode(gpio.BOARD)

  gpio.setup(12, gpio.OUT)
  gpio.setup(11, gpio.OUT)
  gpio.setup(13, gpio.OUT)
  gpio.setup(15, gpio.OUT)

  pwm12 = gpio.PWM(12, 100) # PWM cycle upto 500Hz
  pwm11 = gpio.PWM(11, 100)
  pwm13 = gpio.PWM(13, 100)
  pwm15 = gpio.PWM(15, 100)

def forward(tf):
  global pwm11, pwm12, pwm13, pwm15
  init()

  pwm12.start(0)
  pwm11.start(pr1)
  pwm13.start(pr1)
  pwm15.start(0)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()

def backward(tf):
  init()

  pwm12.start(pr1)
  pwm11.start(0)
  pwm13.start(0)
  pwm15.start(pr1)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()

def left(tf):
  init()
  pwm12.start(0)
  pwm11.start(pr3l)
  pwm13.start(pr2l)
  pwm15.start(0)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()

def right(tf):
  init()
  pwm12.start(0)
  pwm11.start(pr2r)
  pwm13.start(pr3r)
  pwm15.start(0)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()


def ccw(tf):
  init()
  pwm12.start(pr4)
  pwm11.start(0)
  pwm13.start(pr4)
  pwm15.start(0)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()

def cw(tf):
  init()
  pwm12.start(0)
  pwm11.start(pr4)
  pwm13.start(0)
  pwm15.start(pr4)

  if tf > 0:
    time.sleep(tf)
    gpio.cleanup()

def stop():
  init()
  gpio.cleanup()

