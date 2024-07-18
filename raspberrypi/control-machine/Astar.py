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

        self.came_from = {}

        self.path = []

    def euclidean_distance(self, curr, dest):
        x, y = curr
        dest_x, dest_y = dest

        delta_x = dest_x - x
        delta_y = dest_y - y

        return math.sqrt(delta_x**2 + delta_y**2)

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

        # give instructions of going l, r, u, d to follow path

        directions = []

        for i in range(len(self.path) - 1):
            cur_x, cur_y = self.path[i]
            next_x, next_y = self.path[i + 1]

            if cur_x < next_x:
                directions.append("R")
            elif cur_x > next_x:
                directions.append("L")
            elif cur_y < next_y:
                directions.append("D")
            elif cur_y > next_y:
                directions.append("U")

        return directions
