import heapq
import numpy as np

class Astar:
    def __init__(self, row, col, obstacles, start, dest) -> None:
        self._row = row
        self._col = col

        # Convert real-world obstacle coordinates to row-col format
        self._obstacles = {(int(y), int(x)) for x, y in obstacles}

        # Convert start/dest to row-col
        self._start = (int(start[1]), int(start[0]))
        self._dest = (int(dest[1]), int(dest[0]))

        self._visited = set()
        self._heuristic = self.manhattan_distance
        self._heap = [(self._heuristic(self._start), 0, self._start, [self._start])]

    def euclidean_distance(self, curr) -> float:
        x, y = curr
        dest_x, dest_y = self._dest
        return np.linalg.norm([dest_x - x, dest_y - y])

    def manhattan_distance(self, curr) -> float:
        x, y = curr
        dest_x, dest_y = self._dest
        return abs(dest_x - x) + abs(dest_y - y)

    def set_heuristic_method(self, method) -> None:
        self._heuristic = method

    def _is_obstacle(self, r, c) -> bool:
        return (r, c) in self._obstacles

    def _get_neighbors(self, curr):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # (UP, RIGHT, DOWN, LEFT)
        r, c = curr
        neighbors = []
        
        for rdir, cdir in dirs:
            rcal = r + rdir
            ccal = c + cdir
            
            if (
                0 <= rcal < self._row and  # Ensure within row bounds
                0 <= ccal < self._col and  # Ensure within column bounds
                not self._is_obstacle(rcal, ccal) and  # Avoid obstacles
                (rcal, ccal) not in self._visited  # Avoid revisiting
            ):
                neighbors.append((rcal, ccal))

        return neighbors

    def _clear(self):
        self._heap = [(self._heuristic(self._start), 0, self._start, [self._start])]
        self._visited.clear()

    def find_path(self):
        self._clear()
        # Validate start and destination
        if self._is_obstacle(*self._start):
            print("Error: Start position is an obstacle!")
            return []

        if self._is_obstacle(*self._dest):
            print("Error: Destination position is an obstacle!")
            return []

        while self._heap:
            _, depth, curr, path = heapq.heappop(self._heap)

            if curr == self._dest:
                print("Path found!")
                return path

            self._visited.add(curr)
            neighbors = self._get_neighbors(curr)

            if not neighbors:
                print(f"No available neighbors at {curr}. A* stuck.")

            for neighbor in neighbors:
                new_depth = depth + 1
                heapq.heappush(
                    self._heap,
                    (
                        new_depth + self._heuristic(neighbor),
                        new_depth,
                        neighbor,
                        path + [neighbor],
                    ),
                )

        print("No valid path found.")
        return []
