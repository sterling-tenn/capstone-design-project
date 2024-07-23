# MPU6050 gyroscope/accelerometer
# https://docs.sunfounder.com/projects/raphael-kit/en/latest/python_pi5/pi5_2.2.9_mpu6050_module_python.html

# V_cc = 3.3V (physical pin 1)
# GND = GND (physical pin 6)
# SDA = SDA (physical pin 3 / GPIO 2)
# SCL = SCL (physical pin 5 / GPIO 3)

import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
    time.sleep(0.1)
    print("=================================================")
    
    # Read gyroscope data
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    
    # Gyroscope data (degrees per second)
    gyro_xout_scaled = gyro_xout / 131
    gyro_yout_scaled = gyro_yout / 131
    gyro_zout_scaled = gyro_zout / 131
    
    print(f"Gyroscope data:")
    # print(f"  X: {gyro_xout} raw, {gyro_xout_scaled:.2f} deg/s")
    # print(f"  Y: {gyro_yout} raw, {gyro_yout_scaled:.2f} deg/s")
    # print(f"  Z: {gyro_zout} raw, {gyro_zout_scaled:.2f} deg/s")
    print(f"  X: {gyro_xout_scaled:.2f} deg/s")
    print(f"  Y: {gyro_yout_scaled:.2f} deg/s")
    print(f"  Z: {gyro_zout_scaled:.2f} deg/s")

    # Read accelerometer data
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    
    # Accelerometer data (g-forces)
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    
    print(f"Accelerometer data:")
    # print(f"  X: {accel_xout} raw, {accel_xout_scaled:.4f} g")
    # print(f"  Y: {accel_yout} raw, {accel_yout_scaled:.4f} g")
    # print(f"  Z: {accel_zout} raw, {accel_zout_scaled:.4f} g")
    print(f"  X: {accel_xout_scaled:.4f} g")
    print(f"  Y: {accel_yout_scaled:.4f} g")
    print(f"  Z: {accel_zout_scaled:.4f} g")
    
    # Calculate rotation
    x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    
    print(f"Rotation (in degrees):")
    print(f"  X: {x_rotation:.2f}")
    print(f"  Y: {y_rotation:.2f}")
    
    # time.sleep(1)
