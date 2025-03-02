import json
import conf as conf
import math
import numpy as np
import threading
import time
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

    def _read_sensors(self, sensors, collision_event, kill_event):
        while not collision_event.is_set():
            if kill_event.is_set(): return
            c = sensors[0].get_distance()
            l = sensors[1].get_distance()
            r = sensors[2].get_distance()
            # print(f"[Distances] Centre: {c:.2f} cm | Left: {l:.2f} cm | Right: {r:.2f} cm")

            if c < conf.STOP_DISTANCE or l < conf.STOP_DISTANCE_SIDE_SENSORS or r < conf.STOP_DISTANCE_SIDE_SENSORS:
                print("Obstacle detected! Stopping the robot.")
                self.movement.stop()
                collision_event.set()  # This will stop the sensor thread
                self._handle_collision(collision_event)

            time.sleep(0.1)
    
    def _handle_collision(self, collision_event):
        # while True:
        #     collision_event.wait() # Blocks until collision is detected
        print("Executing collision recovery")
        self.movement.move_backward(conf.COLLISION_RECOVERY_MOVEMENT) # Backup a bit
        collision_event.clear() # No longer in threat of collision

    def find_lookahead_point(self, robot_x, robot_y, path):
        min_dist = float('inf')
        lookahead_point = None
        closest_index = None

        # Find the closest waypoint on the path
        for i, (px, py) in enumerate(path):
            dist = np.hypot(px - robot_x, py - robot_y)
            if dist < min_dist:
                min_dist = dist
                closest_index = i

        # Search for a lookahead point **after** the closest point
        for i in range(closest_index + 1, len(path)):
            px, py = path[i]
            dist = np.hypot(px - robot_x, py - robot_y)

            if dist >= conf.LOOKAHEAD_DISTANCE:
                return (px, py)  # Found valid lookahead point

        return None  # No valid point found

        # for px, py in path:
        #     dist = np.hypot(px - robot_x, py - robot_y)
        #     if dist >= conf.LOOKAHEAD_DISTANCE and dist < min_dist:
        #         min_dist = dist
        #         lookahead_point = (px, py)
        # return lookahead_point

    def _move_robot_auto_mcl(self, map_src_file, path_src_file):
        with open(map_src_file, "r") as file:
            map = json.load(file)
        
        with open(path_src_file, "r") as file:
            path_dict = json.load(file)
            path = path_dict["path"]

        collision_event = threading.Event() # Tracks if collision was detected
        kill_event = threading.Event() # Kills all threads
        turn_start_event = threading.Event() # Start of a turn, needed to start capturing gyro data
        turn_end_event = threading.Event() # End of a turn, needed to process gyro data and update current heading

        # print(self.gyro.get_curr_heading())
        # self.movement.turn_right(90, turn_start_event, turn_end_event)
        # # time.sleep(0.1)
        # print(self.gyro.get_curr_heading())
        # self.movement.turn_left(180, turn_start_event, turn_end_event)
        # # time.sleep(0.1)
        # print(self.gyro.get_curr_heading())
        # kill_event.set()
        # return

        sensors = [self._sensor_centre, self._sensor_left, self._sensor_right]
        sensor_thread = threading.Thread(target=self._read_sensors, args=(sensors, collision_event, kill_event))
        gyro_thread = threading.Thread(target=self.gyro._gyro, args=(kill_event, turn_start_event, turn_end_event))
        # collision_handler_thread = threading.Thread(target=self._handle_collision, args=(collision_event))
        sensor_thread.start()
        gyro_thread.start()
        # collision_handler_thread.start()

        # end_coordinates = path[-1]

        
        # curr_position = path[0] # Assume at start current position is the first path coordinate
        # curr_position.append(0)
        self._mcl = MCLocalization(map, [path[0][0], path[0][1], 0])
        collision_check = False

        while True:
            while (collision_event.is_set()):  # Wait until collision_handler thread unsets the collision. MCL should recalculate new heading and distance to next waypoint based on current pos
                collision_check = True
                pass
            
            if (collision_check): # We moved backward, mcl needs to know what change in movement was done. No heading change should have occured
                sensor_readings = [self._sensor_centre, self._sensor_left, self._sensor_right]
                delta_x = -conf.COLLISION_RECOVERY_MOVEMENT * np.cos(self.gyro.get_curr_heading())
                delta_y = -conf.COLLISION_RECOVERY_MOVEMENT * np.sin(self.gyro.get_curr_heading())
                self._mcl.mcl(sensor_readings, [delta_x, delta_y, 0])

            curr_position = self._mcl._get_position_mean()
            
            # print(f'Current Position: {curr_position}')
            # print(f'Current Heading: {self.gyro.get_curr_heading()} deg')

            # 2. Compute Pure Pursuit control
            lookahead = self.find_lookahead_point(curr_position[0], curr_position[1], path)
            if lookahead is None: break;  # No more waypoints
            
            # print(f'Next Waypoint: {lookahead}')
            
            lx, ly = lookahead
            delta_x = lx - curr_position[0]
            delta_y = ly - curr_position[1]
            
            # curr_heading = self.gyro.get_curr_heading()

            theta = self.gyro.get_next_heading(delta_x, delta_y) # Don't need abs for this. atan2 handles it
            print(f'Current Position - x: {curr_position[0]:.2f} y: {curr_position[1]:.2f} | Current Heading - {self.gyro.get_curr_heading():.2f} | Next Waypoint - x: {lookahead[0]:.2f} y: {lookahead[1]:.2f} | Turn towards waypoint: {theta:.2f} deg')

            if theta>0: self.movement.turn_left(theta, turn_start_event, turn_end_event) # https://support.microsoft.com/en-us/office/atan2-function-c04592ab-b9e3-4908-b428-c96b3a565033
            else: self.movement.turn_right(-theta, turn_start_event, turn_end_event)

            distance_to_move = self.gyro.dist(abs(delta_x), abs(delta_y))
            self.movement.move_forward(distance_to_move) # Move
            
            # 3. Apply movement (assume fixed speed) and sensor readingss
            sensor_readings = [self._sensor_centre, self._sensor_left, self._sensor_right]
            self._mcl.mcl(sensor_readings, [delta_x, delta_y, theta])
            collision_check = False

        kill_event.set()
        sensor_thread.join()
        gyro_thread.join()
        print("END")

        ##### END ######

        # theta = self.gyro.get_gyro()[0] # Need current heading x-axis value
        # theta = self.gyro.get_rotation() # Need current heading x-axis value
        # path.pop(0) # Remove starting position
        # next_movement = [abs(path[0][0]-curr_position[0]), abs(path[0][1]-curr_position[1]), theta] # Assume next movement is going to next waypoint. Need all this info for mcl function
        # print(f'Next Waypoint: {path[0]}')
        # print(f'Current Position: {curr_position}')
        # distance_to_move = self.gyro.dist(next_movement[0], next_movement[1]) # Hypontenuse to figure out how far to move
        # # distance_to_move = math.sqrt(next_movement[0]**2, next_movement[1]**2) # Hypontenuse to figure out how far to move

        # while True:
        #     self.movement.move_forward(distance_to_move) # Move

        #     while (collision_event.is_set()): pass # Wait until collision_handler thread unsets the collision. MCL should recalculate new heading and distance to next waypoint based on current pos
            
        #     # Mcl Cycle
        #    # sensor_readings = [self._sensor_centre.get_distance(), self._sensor_left.get_distance(), self._sensor_right.get_distance()]
        #     sensor_readings = [self._sensor_centre, self._sensor_left, self._sensor_right]

        #     curr_position = self._mcl.mcl(sensor_readings, next_movement)

        #     path.pop(0)

        #     if ((curr_position[0] == end_coordinates[0] and curr_position[1] == end_coordinates[1]) or len(path)==0):
        #         kill_event.set() 
        #         break # Reached the end. Should add margin to this for sure
        
        #     print(f'Next Waypoint: {path[0]}')
        #     print(f'Current Position: {curr_position}')

        #     actual_heading = self.gyro.get_rotation()
        #     theta = self.gyro.get_next_heading(path[0][0]-curr_position[0], path[0][1]-curr_position[1], actual_heading) # Don't need abs for this. atan2 handles it
            
        #     if theta>0: 
        #         # print("Turning left")
        #         self.movement.turn_left(theta) # https://support.microsoft.com/en-us/office/atan2-function-c04592ab-b9e3-4908-b428-c96b3a565033
        #     else: 
        #         # print("Turning right")
        #         self.movement.turn_right(-theta)

        #     next_movement = [abs(path[0][0]-curr_position[0]), abs(path[0][1]-curr_position[1]), theta]
        #     distance_to_move = self.gyro.dist(next_movement[0], next_movement[1])

        # print(f'Current Position: {curr_position}')

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
