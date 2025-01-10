import json
import conf as conf
from movement import Movement
from distance_sensor import DistSensor
from gyroscope import Gyro

# MAKE IO ASYNC / CONCURRANT

    # INITIALIZE ROBOT
        # GET MAP
        # GET PATH
        #OPTIONAL: OPTIMIZE PATH

    # WHILE PATH EXISTS
        # PREP SENSOR / MOVEMENT DATA FOR PARTICLE FILTER
        # CONTROLLER / PARTICLE FILTER
        # OPTIONAL: UPDATE MAP (parallel with particle filter for foreign obstacles, needs to update path)
        # GET BEST NEXT MOVEMENT VIA PARTICLE FILTER LOC AND UPDATED PATH
        # EXECUTE MOVEMENT
    # RESET TO NEW PATH

class RobotController:
    def __init__(self):
        # Initialize the Movement class to control the servos
        self.movement = Movement()
        self.gyro = Gyro(conf.GYRO_SENSOR_ID)
        self._sensor_centre = DistSensor(conf.TRIGGER_PIN_CENTRE, conf.ECHO_PIN_CENTRE, conf.CENTOR_SENSOR_ID)
        self._sensor_left = DistSensor(conf.TRIGGER_PIN_LEFT, conf.ECHO_PIN_LEFT, conf.LEFT_SENSOR_ID)
        self._sensor_right = DistSensor(conf.TRIGGER_PIN_RIGHT, conf.ECHO_PIN_RIGHT, conf.RIGHT_SENSOR_ID)

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

            match direction:
                case "L":
                    print("Turning left")
                    self.movement.turn_left(90)
                case "R":
                    print("Turning right")
                    self.movement.turn_right(90)
                case "F":
                    print("Moving forward")
                    self.movement.move_forward(conf.BLOCK_SIZE)
                case _:
                    raise ValueError("Unknown direction.")

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
            match char:
                case 'w':
                    print("Moving Forward")
                    self.movement.move_forward(conf.BLOCK_SIZE)
                case 's':
                    print("Moving Backward")
                    self.movement.move_backward(conf.BLOCK_SIZE)
                case 'a':
                    print("Turning Left")
                    self.movement.turn_left(90)
                case 'd':
                    print("Turning Right")
                    self.movement.turn_right(90)
                case 't':
                    print("Stopping")
                    self.movement.stop()
                case 'q':
                    print("Exiting manual mode")
                    break
                case _:
                    raise ValueError("Unsupported input")
    
    def run(self, mode, file_path=None):
        try:
            input("Press Enter to start the automatic movement sequence")

            match mode:
                case 'auto':
                    if file_path is None:
                        raise ValueError("File path is required for auto mode")
                    self._move_robot_auto(file_path)
                case 'manual':
                    self._move_robot_manual()
                case _:
                    raise ValueError("Unsupported mode")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
        finally:
            self.movement.stop()
            self._sensor_centre.close()
            self._sensor_left.close()
            self._sensor_right.close()
