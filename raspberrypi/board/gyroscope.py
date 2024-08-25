from smbus2 import SMBus
import math as m
import numpy as np
import time as t

class Gyro:

    def __init__(self) -> None:
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c

        # This is the address value read via the i2cdetect command
        self.address = 0x68         

        # The gyroscope output data registers
        self.gyro_xout_addr = 0x43
        self.gyro_yout_addr = 0x45
        self.gyro_zout_addr = 0x47

        # The accelerometer output data registers
        self.accel_xout_addr = 0x3b
        self.accel_yout_addr = 0x3d
        self.accel_zout_addr = 0x3f

        # SMBus init
        self.bus = SMBus(1)
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)    

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return m.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x, y, z):
        radians = m.atan2(x, self.dist(y, z))
        return -m.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = m.atan2(y, self.dist(x, z))
        return m.degrees(radians)

    def get_accel_out(self):
        xout = self.read_word_2c(self.accel_xout_addr)
        yout = self.read_word_2c(self.accel_yout_addr)
        zout = self.read_word_2c(self.accel_zout_addr)
        return np.array([xout, yout, zout])
    
    def get_gyro_out(self):
        xout = self.read_word_2c(self.gyro_xout_addr)
        yout = self.read_word_2c(self.gyro_yout_addr)
        zout = self.read_word_2c(self.gyro_zout_addr)
        return np.array([xout, yout, zout])
    
    def get_accel_scaled(self):
        # Convert to m/s^2 assuming the scale factor is 16384 LSB/g
        return self.get_accel_out() * 9.80665 / 16384.0

    def get_gyro_scaled(self):
        # Convert to degrees per second assuming the scale factor is 131 LSB/(°/s)
        return self.get_gyro_out() / 131.0
    

gyro = Gyro()

while True:
    print("=================================================")
    
    # Get scaled gyro data
    gyro_scaled = gyro.get_gyro_scaled()
    gyro_xout_scaled = gyro_scaled[0]
    gyro_yout_scaled = gyro_scaled[1]
    gyro_zout_scaled = gyro_scaled[2]

    # Get scaled accelerometer data
    accel_scaled = gyro.get_accel_scaled()
    accel_xout_scaled = accel_scaled[0]
    accel_yout_scaled = accel_scaled[1]
    accel_zout_scaled = accel_scaled[2]

    # Calculate rotations
    x_rotation = gyro.get_x_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
    y_rotation = gyro.get_y_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
    
    # Print gyroscope data
    print("Gyroscope data:")
    print(f"  X: {gyro_xout_scaled:.2f} deg/s")
    print(f"  Y: {gyro_yout_scaled:.2f} deg/s")
    print(f"  Z: {gyro_zout_scaled:.2f} deg/s")

    # Print accelerometer data
    print("Accelerometer data:")
    print(f"  X: {accel_xout_scaled:.4f} m/s^2")
    print(f"  Y: {accel_yout_scaled:.4f} m/s^2")
    print(f"  Z: {accel_zout_scaled:.4f} m/s^2")
    
    # Print rotation data
    print("Rotation (in degrees):")
    print(f"  X: {x_rotation:.2f}")
    print(f"  Y: {y_rotation:.2f}")
    
    t.sleep(1)
