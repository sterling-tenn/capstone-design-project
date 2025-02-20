# configuration variables

# Servo pins
LEFT_SERVO_PIN      = 27 # GPIO 27, physical pin 13
RIGHT_SERVO_PIN     = 17 # GPIO 17, physical pin 11

# Sensor pins
TRIGGER_PIN_CENTRE  = 23 # GPIO 23, physical pin 16
ECHO_PIN_CENTRE     = 24 # GPIO 24, physical pin 18

TRIGGER_PIN_LEFT    = 5 # GPIO 5, physical pin 29
ECHO_PIN_LEFT       = 6 # GPIO 6, physical pin 31

TRIGGER_PIN_RIGHT   = 13 # GPIO 13, physical pin 33
ECHO_PIN_RIGHT      = 19 # GPIO 19, physical pin 35

# Gyro pins
PWR_MGMT_1      = 0x6b
PWR_MGMT_2      = 0x6c

GYRO_ADDRESS    = 0x68         

GYRO_XOUT_ADDR  = 0x43
GYRO_YOUT_ADDR  = 0x45
GYRO_ZOUT_ADDR  = 0x47

ACCEL_XOUT_ADDR = 0x3b
ACCEL_YOUT_ADDR = 0x3d
ACCEL_ZOUT_ADDR = 0x3f

TEMP_OUT_ADDR   = 0x41

GYRO_SMBUS_NUMBER = 1

# misc variables
STOP_DISTANCE   = 20 # in cm, stop if sensors detect an object within this distance
BLOCK_SIZE      = 0.1 # in m, size of a block on the grid/map
TIME_DELTA      = 0.001 # stall time in sec

# physical constants
WHEEL_RADIUS            = 0.037 # radius of wheels in metres
INTERNAL_TURN_RADIUS    = 0.205 # distance between centre and wheels in metres
ANGULAR_VELOCITY        = 6  # wheel/servo angular velocity in rad/s

# particle filter
INIT_POS_SIGMA = 2 # standard deviation of initial position in map
SENSOR_SIGMA = 0.05 # standard deviation of sensor noise
NULL_WEIGHT  = 0.0001
MAP_SCALE = 1.0

# Sensor IDs
CENTOR_SENSOR_ID    = 0
RIGHT_SENSOR_ID     = 1
LEFT_SENSOR_ID      = 2
GYRO_SENSOR_ID      = 4
