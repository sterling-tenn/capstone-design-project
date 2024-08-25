import heapq
import math


class Astar:
    def __init__(self, row, col, obstacles, start, dest):
        self.row = row
        self.col = col
        self.start = start
        self.dest = dest
        self.obstacles = set(obstacles)

        self.g_score = {}
        self.f_score = {}
        self.closed = set()
        self.open = []

        # TODO: initially, we are just going to assume initial north bearing
        self.orientation = "N"
        self.came_from = {}

        self.path = []

    def euclidean_distance(self, curr, dest):
        x, y = curr
        dest_x, dest_y = dest

        delta_x = dest_x - x
        delta_y = dest_y - y

        return math.sqrt(delta_x**2 + delta_y**2)
    
    def manhattan_distance(self, curr, dest):
        x, y = curr
        dest_x, dest_y = dest

        delta_x = dest_x - x
        delta_y = dest_y - y

        return delta_x + delta_y

    def reconstruct_path(self, current):
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path

    def is_obstacle(self, r, c):
        return (r, c) in self.obstacles

    def available_neighbors(self, curr):
        # down, right, up, left
        # no diagonals

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        r, c = curr

        neighbors = []

        for rdir, cdir in dirs:
            rcal = r + rdir
            ccal = c + cdir

            if (
                0 <= ccal < self.col
                and 0 <= rcal < self.row
                and not self.is_obstacle(rcal, ccal)
                and (rcal, ccal) not in self.closed
            ):
                neighbors.append((rcal, ccal))

        return neighbors

    def clear(self):
        self.g_score = {}
        self.f_score = {}
        self.closed = set()
        self.open = []
        self.came_from = {}
        self.path = []

    def find_path(self):
        self.clear()

        starting_h_score = self.euclidean_distance(self.start, self.dest)
        starting_g_score = 0
        starting_f_score = starting_h_score + starting_g_score

        self.g_score[self.start] = 0
        self.f_score[self.start] = starting_f_score

        self.open = [(starting_f_score, self.start)]
        heapq.heapify(self.open)

        while self.open:
            curr = heapq.heappop(self.open)[1]

            self.closed.add(curr)

            if curr == self.dest:
                self.path = self.reconstruct_path(curr)
                return self.path

            neighbors = self.available_neighbors(curr)

            neighbors_cost = self.g_score[curr] + 1

            for neighbor in neighbors:
                if (
                    neighbor not in self.g_score
                    or self.g_score[neighbor] > neighbors_cost
                ):
                    self.came_from[neighbor] = curr
                    self.g_score[neighbor] = neighbors_cost
                    self.f_score[neighbor] = (
                        self.euclidean_distance(neighbor, self.dest)
                        + self.g_score[neighbor]
                    )
                    heapq.heappush(self.open, (self.f_score[neighbor], neighbor))

        return []

    def find_directions(self):
        if not self.path:
            print("Path is not defined, invoke find path function")
            return

        # Orientation mapping
        # from North, a left turn means we go west for example
        left_turns = {"N": "W", "W": "S", "S": "E", "E": "N"}
        right_turns = {"N": "E", "E": "S", "S": "W", "W": "N"}

        directions = []

        for i in range(len(self.path) - 1):
            cur_x, cur_y = self.path[i]
            next_x, next_y = self.path[i + 1]

            if cur_x < next_x:
                desired_orientation = "E"
            elif cur_x > next_x:
                desired_orientation = "W"
            elif cur_y < next_y:
                desired_orientation = "S"
            elif cur_y > next_y:
                desired_orientation = "N"

            # Adjust orientation to the desired one
            while self.orientation != desired_orientation:

                one_left_from_desired = (
                    self.orientation == left_turns[desired_orientation]
                )
                two_rights_from_desired = (
                    self.orientation == right_turns[right_turns[desired_orientation]]
                )

                if one_left_from_desired or two_rights_from_desired:
                    directions.append("R")
                    self.orientation = right_turns[self.orientation]
                else:
                    directions.append("L")
                    self.orientation = left_turns[self.orientation]

            # Move forward
            directions.append("F")

        return directions
