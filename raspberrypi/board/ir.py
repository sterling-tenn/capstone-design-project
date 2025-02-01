# ADJUST KNOB ON SENSOR TO ADJUST SENSITIVITY

from gpiozero import LineSensor
from signal import pause
from conf import *

sensor = LineSensor(IR_SENSOR_PIN)
sensor.when_line = lambda: print('Line detected')
sensor.when_no_line = lambda: print('No line detected')
pause()