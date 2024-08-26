import heapq
import math

class AStar:
    def __init__(self, rows, cols, obstacles, start, dest, mode=1):
        self._rows = rows
        self._cols = cols
        self._obstacles = set(obstacles)
        self._start = start
        self._dest = dest
        self._mode = mode  # 1 for Manhattan, 2 for Euclidean
        
        self._g_score = {}
        self._f_score = {}
        self._visited = set()
        self._open_heap = []
        self._came_from = {}

    def _heuristic(self, node, end) -> float:
        if self._mode == 1:
            return self._manhattan_distance(node, end)  
        elif self._mode == 2:
            return self._euclidean_distance(node, end) 

    def _manhattan_distance(self, node, end) -> int:
        return abs(end[0] - node[0]) + abs(end[1] - node[1])

    def _euclidean_distance(self, node, end) -> float:
        return math.sqrt((end[0] - node[0])**2 + (end[1] - node[1])**2)

    def _is_obstacle(self, r, c) -> bool:
        return (r, c) in self._obstacles

    def _available_neighbors(self, r, c) -> list:
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for rdir, cdir in dirs:
            rcal = r + rdir
            ccal = c + cdir
            if 0 <= rcal < self._rows and 0 <= ccal < self._cols and not self._is_obstacle(rcal, ccal):
                neighbors.append((rcal, ccal))
        return neighbors

    def _reconstruct_path(self, current) -> list:
        path = [current]
        while current in self._came_from:
            current = self._came_from[current]
            path.append(current)
        path.reverse()
        return path

    def find_path(self) -> list:
        self._g_score[self._start] = 0
        self._f_score[self._start] = self._heuristic(self._start, self._dest)
        heapq.heappush(self._open_heap, (self._f_score[self._start], self._start))

        while self._open_heap:
            _, current = heapq.heappop(self._open_heap)
            self._visited.add(current)

            if current == self._dest:
                return self._reconstruct_path(current)
                
            for neighbor in self._available_neighbors(*current):
                next_cost = self._g_score.get(current, 0) + 1
                if (neighbor not in self._g_score) or (next_cost < self._g_score[neighbor]):
                    self._came_from[neighbor] = current
                    self._g_score[neighbor] = next_cost
                    self._f_score[neighbor] = next_cost + self._heuristic(neighbor, self._dest)
                    heapq.heappush(self._open_heap, (self._f_score[neighbor], neighbor))

        return None
