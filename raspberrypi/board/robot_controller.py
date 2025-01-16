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
            if (self._sensor_centre.is_collision_detected() or 
                self._sensor_left.is_collision_detected() or 
                self._sensor_right.is_collision_detected()):
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
        import select

        def getch():
            """Get a single character from standard input."""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                if select.select([sys.stdin], [], [], 0.1)[0]:  # Non-blocking check for keypress
                    return sys.stdin.read(1)
                else:
                    return None
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        print(
            "Manual mode active." 
            "\nHold: "
            "\n\t'W' to move forward," 
            "\n\t'S' to move backward," 
            "\n\t'A' to turn left," 
            "\n\t'D' to turn right." 
            "\nRelease to stop." 
            "\nPress 'Q' to exit."
        )

        current_command = None

        while True:
            char = getch()

            if char:
                char = char.lower()
                if char == 'w':
                    current_command = 'w'
                    self.movement._move_forward_logic()
                elif char == 's':
                    current_command = 's'
                    self.movement._move_backward_logic()
                elif char == 'a':
                    current_command = 'a'
                    self.movement._turn_left_logic()
                elif char == 'd':
                    current_command = 'd'
                    self.movement._turn_right_logic()
                elif char == 'q':
                    print("\nExiting manual mode")
                    break
            else:
                # If no key is pressed or released, stop movement
                if current_command:
                    print("Stopping", end="\r")
                    self.movement.stop()
                    current_command = None

    def run(self, mode, file_path=None):
        try:
            match mode:
                case 'auto':
                    input("Press Enter to start the automatic movement sequence")
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
