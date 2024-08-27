# pin configuration variables

# Servo pins
LEFT_SERVO_PIN = 27 # GPIO 27, physical pin 13
RIGHT_SERVO_PIN = 17 # GPIO 17, physical pin 11

# Sensor pins
TRIGGER_PIN_CENTRE = 23 # GPIO 23, physical pin 16
ECHO_PIN_CENTRE = 24 # GPIO 24, physical pin 18

TRIGGER_PIN_LEFT = 5 # GPIO 5, physical pin 29
ECHO_PIN_LEFT = 6 # GPIO 6, physical pin 31

TRIGGER_PIN_RIGHT = 13 # GPIO 13, physical pin 33
ECHO_PIN_RIGHT = 19 # GPIO 19, physical pin 35

STOP_DISTANCE = 20 # in cm, stop if sensors detect an object within this distance

BLOCK_SIZE = 0.25 # in m, size of a block on the grid/map
TIME_DELTA = 0.01 # stall time in sec