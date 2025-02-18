import json
import conf as conf
import math
from movement import Movement
from distance_sensor import DistSensor
from gyroscope import Gyro
from mc_localization import MCLocalization

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

    def _move_robot_auto_mcl(self, map_src_file, path_src_file):
        with open(map_src_file, "r") as file:
            map = json.load(file)
        
        with open(path_src_file, "r") as file:
            path_dict = json.load(file)
            path = path_dict["path"]

        end_coordinates = path[-1]

        
        curr_position = path[0] # Assume at start current position is the first path coordinate
        curr_position.append(0)
        print(curr_position)
        self._mcl = MCLocalization(map, curr_position)

        theta = self.gyro.get_gyro()[0] # Need current heading x-axis value
        path.pop(0) # Remove starting position
        next_movement = [abs(path[0][0]-curr_position[0]), abs(path[0][1]-curr_position[1]), theta] # Assume next movement is going to next waypoint. Need all this info for mcl function
        distance_to_move = self.gyro.dist(next_movement[0], next_movement[1]) # Hypontenuse to figure out how far to move
        # distance_to_move = math.sqrt(next_movement[0]**2, next_movement[1]**2) # Hypontenuse to figure out how far to move

        while True:
            self.movement.move_forward(distance_to_move) # Move
            path.pop(0)
            
            # Mcl Cycle
           # sensor_readings = [self._sensor_centre.get_distance(), self._sensor_left.get_distance(), self._sensor_right.get_distance()]
            sensor_readings = [self._sensor_centre, self._sensor_left, self._sensor_right]

            curr_position = self._mcl.mcl(sensor_readings, next_movement)
            print(curr_position)
            print(path[0])

            if ((curr_position[0] == end_coordinates[0] and curr_position[1] == end_coordinates[1]) or len(path)==0): break # Reached the end. Should add margin to this for sure

            theta = self.gyro.get_next_heading(path[0][0]-curr_position[0], path[0][1]-curr_position[1], curr_position[2]) # Don't need abs for this. atan2 handles it
            
            if theta>0: self.movement.turn_left(theta) # https://support.microsoft.com/en-us/office/atan2-function-c04592ab-b9e3-4908-b428-c96b3a565033
            else: self.movement.turn_right(-theta)

            next_movement = [abs(path[0][0]-curr_position[0]), abs(path[0][1]-curr_position[1]), theta]
            distance_to_move = self.gyro.dist(next_movement[0], next_movement[1])

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

    def run(self, mode, path=None, map=None):
        try:
            match mode:
                case 'auto_mcl':
                    input("Press Enter to start the automatic mcl movement sequence")
                    if path is None:
                        raise ValueError("Path is required for auto mcl mode")
                    if map is None:
                        raise ValueError("Map is required for auto mcl mode")
                    self._move_robot_auto_mcl(map, path)

                case 'auto':
                    input("Press Enter to start the automatic movement sequence")
                    if path is None:
                        raise ValueError("File path is required for auto mode")
                    self._move_robot_auto(path)

                case 'manual':
                    self._move_robot_manual()

                case _:
                    raise ValueError("Unsupported mode")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
        finally:
            self.movement.stop()
