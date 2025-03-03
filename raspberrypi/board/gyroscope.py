from smbus2 import SMBus
import math as m
import numpy as np
import conf as conf
import threading
import time as t

class Gyro:

    def __init__(self, id) -> None:
        self.id = id

        # Power management registers
        self.power_mgmt_1 = conf.PWR_MGMT_1
        self.power_mgmt_2 = conf.PWR_MGMT_2

        # MPU6050 I2C address
        self.address = conf.GYRO_ADDRESS        

        # Gyroscope output data registers
        self.gyro_xout_addr = conf.GYRO_XOUT_ADDR
        self.gyro_yout_addr = conf.GYRO_YOUT_ADDR
        self.gyro_zout_addr = conf.GYRO_ZOUT_ADDR

        # Accelerometer output data registers
        self.accel_xout_addr = conf.ACCEL_XOUT_ADDR
        self.accel_yout_addr = conf.ACCEL_YOUT_ADDR
        self.accel_zout_addr = conf.ACCEL_ZOUT_ADDR

        # Temperature output data register
        self.temp_out_addr = conf.TEMP_OUT_ADDR

        # SMBus initialization
        self.bus = SMBus(conf.GYRO_SMBUS_NUMBER)
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)    

        # Heading
        self.curr_heading = conf.STARTING_HEADING

    def read_byte(self, adr) -> int:
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr) -> int:
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr) -> int:
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b) -> float:
        return m.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z) -> float:
        radians = m.atan2(x, self.dist(y, z))
        return -m.degrees(radians)

    def get_x_rotation(self, x, y, z) -> float:
        radians = m.atan2(y, self.dist(x, z))
        return m.degrees(radians)

    def get_z_rotation(self, x, y, z) -> float:
        radians = m.atan2(z, self.dist(x, y))
        return m.degrees(radians)
    
    def get_next_heading(self, delta_x, delta_y) -> float:
        radians = m.atan2(delta_y, delta_x)
        desired_heading = m.degrees(radians)
        return desired_heading-self.curr_heading

    def get_accel(self) -> np.ndarray:
        xout = self.read_word_2c(self.accel_xout_addr)
        yout = self.read_word_2c(self.accel_yout_addr)
        zout = self.read_word_2c(self.accel_zout_addr)
        return np.array([xout, yout, zout])
    
    def get_gyro(self) -> np.ndarray:
        xout = self.read_word_2c(self.gyro_xout_addr)
        yout = self.read_word_2c(self.gyro_yout_addr)
        zout = self.read_word_2c(self.gyro_zout_addr)
        return np.array([xout, yout, zout])

    def get_rotation(self) -> float:
        values = self.get_gyro()
        return self.get_x_rotation(values[0], values[1], values[2])
    
    def get_accel_scaled(self) -> np.ndarray:
        # Convert to m/s^2 assuming the scale factor is 16384 LSB/g
        return self.get_accel() * 9.80665 / 16384.0

    def get_gyro_scaled(self) -> np.ndarray:
        # Convert to degrees per second assuming the scale factor is 131 LSB/(°/s)
        return self.get_gyro() / 131.0
    
    def get_temp(self) -> float:
        # Convert to degrees Celsius
        return self.read_word_2c(self.temp_out_addr) / 340.0 + 36.53

    def get_id(self) -> int:
        return self.id

    def get_curr_heading(self):
        return self.curr_heading

    def _gyro(self, kill_event, turn_start_event, turn_end_event):
        y_readings = 0
        y_num_readings = 0
        start_time = 0
        while True:
            if (kill_event.is_set()): return # Exit the thread
            
            if turn_start_event.is_set(): # Turn has started, collect angular momentum readings and number of readings done
                if (y_num_readings==0): start_time = t.time()
                y_readings += self.get_gyro_scaled()[1] #Scaled y (yaw) angular momentum in deg/s
                y_num_readings = y_num_readings + 1
            
            if (turn_end_event.is_set()): # Turn has ended calculate average angular momentum, multiply by time elapsed to get rotation. Update current heading
                time_elapsed = t.time() - start_time
                self.curr_heading -= (y_readings/y_num_readings) * time_elapsed
                y_readings = 0
                y_num_readings = 0
                turn_end_event.clear()

    def _data(self, kill_event, turn_start_event, turn_end_event):
        import os
        # import time as t

        # Run the program to test
        # gyro = Gyro(conf.GYRO_SENSOR_ID)
        curr_heading = 0
        y_readings = 0
        y_num_readings = 0
        start_time = 0
        while True:
            # Get scaled gyro data
            if (kill_event.is_set()): return
            
            if turn_start_event.is_set():
                if (y_num_readings==0): 
                    start_time = t.time()
                y_readings += self.get_gyro_scaled()[1]
                y_num_readings = y_num_readings + 1
            
            if (turn_end_event.is_set()):
                time_elapsed = t.time() - start_time
                curr_heading += (y_readings/y_num_readings) * time_elapsed
                y_readings = 0
                y_num_readings = 0
                turn_end_event.clear()

            gyro_scaled = self.get_gyro_scaled()
            gyro_xout_scaled = gyro_scaled[0]
            gyro_yout_scaled = gyro_scaled[1]
            gyro_zout_scaled = gyro_scaled[2]

            # Get scaled accelerometer data
            accel_scaled = self.get_accel_scaled()
            accel_xout_scaled = accel_scaled[0]
            accel_yout_scaled = accel_scaled[1]
            accel_zout_scaled = accel_scaled[2]

            # Calculate rotations
            x_rotation = self.get_x_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
            y_rotation = self.get_y_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
            z_rotation = self.get_z_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])

            # Calculate temperature
            temp = self.get_temp()

            os.system('cls' if os.name == 'nt' else 'clear')
            print("=================================================")
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
            print(f"  Z: {z_rotation:.2f}")

            # Print temperature data
            print("Temperature (in Celsius):")
            print(f"  T: {temp:.2f}")

            print("Current Heading (in degrees):")
            print(f"  T: {curr_heading:.2f}")

            print("=================================================")
            t.sleep(0.1)

if __name__ == "__main__":

    from movement import Movement

    kill_event = threading.Event()
    turn_start_event = threading.Event()
    turn_end_event = threading.Event()
    gyro = Gyro(conf.GYRO_SENSOR_ID)
    movement = Movement()
    data_thread = threading.Thread(target=gyro._data, args=(kill_event, turn_start_event, turn_end_event))
    data_thread.start()

    turn_start_event.set()
    movement.turn_right(90)
    turn_start_event.clear()
    turn_end_event.set()
    t.sleep(5)
    turn_start_event.set()
    movement.turn_left(135)
    turn_start_event.clear()
    turn_end_event.set()
    t.sleep(5)
    kill_event.set()
    data_thread.join()

    # import os
    # import time as t

    # # Run the program to test
    # gyro = Gyro(conf.GYRO_SENSOR_ID)
    
    # while True:
    #     # Get scaled gyro data
    #     gyro_scaled = gyro.get_gyro_scaled()
    #     gyro_xout_scaled = gyro_scaled[0]
    #     gyro_yout_scaled = gyro_scaled[1]
    #     gyro_zout_scaled = gyro_scaled[2]

    #     # Get scaled accelerometer data
    #     accel_scaled = gyro.get_accel_scaled()
    #     accel_xout_scaled = accel_scaled[0]
    #     accel_yout_scaled = accel_scaled[1]
    #     accel_zout_scaled = accel_scaled[2]

    #     # Calculate rotations
    #     x_rotation = gyro.get_x_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
    #     y_rotation = gyro.get_y_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])
    #     z_rotation = gyro.get_z_rotation(accel_scaled[0], accel_scaled[1], accel_scaled[2])

    #     # Calculate temperature
    #     temp = gyro.get_temp()

    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     print("=================================================")
    #     # Print gyroscope data
    #     print("Gyroscope data:")
    #     print(f"  X: {gyro_xout_scaled:.2f} deg/s")
    #     print(f"  Y: {gyro_yout_scaled:.2f} deg/s")
    #     print(f"  Z: {gyro_zout_scaled:.2f} deg/s")

    #     # Print accelerometer data
    #     print("Accelerometer data:")
    #     print(f"  X: {accel_xout_scaled:.4f} m/s^2")
    #     print(f"  Y: {accel_yout_scaled:.4f} m/s^2")
    #     print(f"  Z: {accel_zout_scaled:.4f} m/s^2")
        
    #     # Print rotation data
    #     print("Rotation (in degrees):")
    #     print(f"  X: {x_rotation:.2f}")
    #     print(f"  Y: {y_rotation:.2f}")
    #     print(f"  Z: {z_rotation:.2f}")

    #     # Print temperature data
    #     print("Temperature (in Celsius):")
    #     print(f"  T: {temp:.2f}")

    #     print("=================================================")
    #     t.sleep(0.1)
