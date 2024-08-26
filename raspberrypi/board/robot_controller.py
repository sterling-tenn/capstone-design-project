import json
import conf as conf
from movement import Movement
from distance_sensor import DistSensor
from gyroscope import Gyro

class RobotController:
    def __init__(self):
        # Initialize the Movement class to control the servos
        self.movement = Movement()
        self.gyro = Gyro()
        self._sensor_centre = DistSensor(conf.TRIGGER_PIN_CENTRE, conf.ECHO_PIN_CENTRE, "Centre Sensor")
        self._sensor_left = DistSensor(conf.TRIGGER_PIN_LEFT, conf.ECHO_PIN_LEFT, "Left Sensor")
        self._sensor_right = DistSensor(conf.TRIGGER_PIN_RIGHT, conf.ECHO_PIN_RIGHT, "Right Sensor")

    def _move_robot_auto(self, source_file):
        with open(source_file, "r") as file:
            data = json.load(file)
            directions = data["directions"]

        for direction in directions:
            if (self._sensor_centre.collision_detected() or 
                self._sensor_left.collision_detected() or 
                self._sensor_right.collision_detected()):
                print("Collision detected! Stopping the robot.")
                self.movement.stop()
                break

            if direction == "L":
                print("Turning left")
                self.movement.turn_left(90)
            elif direction == "R":
                print("Turning right")
                self.movement.turn_right(90)
            elif direction == "F":
                print("Moving forward")
                self.movement.move_forward(conf.BLOCK_SIZE)

    def _move_robot_manual(self):
        import sys
        import termios
        import tty
        
        def getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

        print("Manual mode active. Use 'W' to move forward, 'S' to move backward, 'A' to turn left, 'D' to turn right, 'T' to stop, and 'Q' to exit.")

        while True:
            char = getch().lower()
            if char == 'w':
                print("Moving Forward")
                self.movement.move_forward(conf.BLOCK_SIZE)
            elif char == 's':
                print("Moving Backward")
                self.movement.move_backward(conf.BLOCK_SIZE)
            elif char == 'a':
                print("Turning Left")
                self.movement.turn_left(90)
            elif char == 'd':
                print("Turning Right")
                self.movement.turn_right(90)
            elif char == 't':
                print("Stopping")
                self.movement.stop()
            elif char == 'q':
                print("Exiting manual mode")
                break
    
    def run(self, mode):
        try:
            input("Press Enter to start the automatic movement sequence")

            if mode == 1:
                self._move_robot_auto("path.json")
            elif mode == 2:
                self._move_robot_manual()

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
        finally:
            self.movement.stop()
            self._sensor_centre.close()
            self._sensor_left.close()
            self._sensor_right.close()

