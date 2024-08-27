import heapq
import numpy as np
from celltype import CellType

class Astar:
    def __init__(self, row, col, obstacles, start, dest) -> None:
        self._row = row
        self._col = col
        self._start = start
        self._dest = dest
        self._obstacles = set(obstacles)

        # heap_node -> [cost, depth, node, path]
        self._visited = set()
        self._heuristic = self.manhattan_distance
        self._heap = [(self._heuristic(self._start), 0, self._start, [self._start])]

    def euclidean_distance(self, curr) -> float:
        x, y = curr
        dest_x, dest_y = self._dest
        delta_x = dest_x - x
        delta_y = dest_y - y
        return np.linalg.norm([delta_x, delta_y])
    
    def manhattan_distance(self, curr) -> float:
        x, y = curr
        dest_x, dest_y = self._dest
        delta_x = dest_x - x
        delta_y = dest_y - y
        return abs(delta_x) + abs(delta_y)
    
    def set_heuristic_method(self, method) -> None:
            self._integration_method = method

    def _is_obstacle(self, r, c):
        return (r, c) in self._obstacles

    def _get_neighbors(self, curr):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        r, c = curr
        neighbors = []
        for rdir, cdir in dirs:
            rcal = r + rdir
            ccal = c + cdir
            if (
                0 <= ccal < self._col and 0 <= rcal < self._row
                and not self._is_obstacle(rcal, ccal)
                and (rcal, ccal) not in self._visited
            ):
                neighbors.append((rcal, ccal))
        return neighbors

    def _clear(self):
        self._heap = [(self._heuristic(self._start), 0, self._start, [self._start])]

    def find_path(self):
        self._clear()
        while self._heap:
            _, depth, curr, path = heapq.heappop(self._heap)
            
            if curr == self._dest:
                return path
            
            self._visited.add(curr)
            neighbors = self._get_neighbors(curr)
            
            for neighbor in neighbors:
                new_depth = depth + 1
                heapq.heappush(
                    self._heap, 
                    (new_depth + self._heuristic(neighbor), new_depth, neighbor, path + [neighbor])
                )
        return []

    def find_directions(self, path, orientation='N'):
        # from North, a left turn means we go west for example
        clkwise_turn = {"N", "E", "S", "W"}
        directions = []
        prev_x, prev_y = path[0]

        for x, y in path[1:]:
            if prev_y > y:
                desired_orientation = "N"
            elif prev_x < x:
                desired_orientation = "E"
            elif prev_y < y:
                desired_orientation = "S"
            elif prev_x > x:
                desired_orientation = "W"
            
            # Adjust orientation to the desired one
            if orientation != desired_orientation:
                curr_index = clkwise_turn.index(orientation)
                cw_index = (curr_index + 1) % 4
                ccw_index = (curr_index - 1) % 4
            
                if desired_orientation == clkwise_turn[cw_index]:
                    directions.append("R")
                elif desired_orientation == clkwise_turn[ccw_index]:
                    directions.append("L")
                else:
                    directions.append("R")
                    directions.append("R")
            
                orientation = desired_orientation
            
            prev_x, prev_y = x, y

            # Move forward
            directions.append("F")

        return directions
